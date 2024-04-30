import pytest
from prepare import *
# 一定写在前面


from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
# 后文出现的该函数名会自动被pytest调用该函数并传入测试用例

def register_login_user(client, mock_user_data):
    os.environ["CHECKCODE"] = mock_user_data["checkCode"]
    client.post("/sendCheckCode", json={"email": mock_user_data["email"]})
    client.post("/registerUser", json=mock_user_data)
    response = client.put("/login", json=mock_user_data)
    assert response.status_code == 200


def test_register_success(mock_user_data, new_database):
    os.environ["CHECKCODE"] = mock_user_data["checkCode"]
    client.post("/sendCheckCode", json = {"email": mock_user_data["email"]})
    # 测试用户注册成功的情况
    response = client.post("/registerUser", json=mock_user_data)
    assert response.status_code == 200
    assert response.json() == {"isSuccess": True}

def test_register_failure(mock_user_data, new_database):
    os.environ["CHECKCODE"] = mock_user_data["checkCode"]
    client.post("/sendCheckCode", json = {"email": mock_user_data["email"]})
    # 测试用户注册失败的情况（用户已存在）
    response1 = client.post("/registerUser", json=mock_user_data)  # 首次注册应该成功
    response = client.post("/registerUser", json=mock_user_data)  # 重复注册应该失败
    assert response.status_code == 400

def test_login(mock_user_data):
    # 测试用户登录成功的情况
    response = client.put("/login", json=mock_user_data)
    assert response.status_code == 200

def test_login_failure(mock_user_data):
    # 测试用户登录失败的情况
    wrong_data = {
        "email": mock_user_data["email"],
        "password": "wrongpassword"
    }
    response = client.put("/login", json=wrong_data)
    assert response.status_code == 400

def test_login_cookie(mock_user_data):
    client.put("/login", json=mock_user_data)
    res = client.get("check_login_state")
    assert res.json()['email'] == mock_user_data["email"]
    assert res.json()['username'] == mock_user_data["username"]
    
def test_follow_and_search(mock_user_data, new_database):
    register_login_user(client, mock_user_data)
    user1 = client.get("check_login_state").json()
    assert user1['email'] == mock_user_data["email"]
    mock_user_data["email"] = "123"+mock_user_data["email"]
    mock_user_data['username'] += '6666'
    register_login_user(client, mock_user_data)
    user2 = client.get("check_login_state").json()
    assert user2['email'] == mock_user_data["email"]
    res = client.get("/queryStar", params={"email1":user2["email"], "email2":user1["email"]}).json()
    assert res['isStar'] == False
    client.post("/setStarState", json={'email1': user2['email'], 'email2': user1['email'],
                                       'state':True})
    res = client.get("/queryStar", params={"email1": user2["email"], "email2": user1["email"]}).json()
    assert res['isStar'] == True
    res = client.get("/getFansByEmail", params={'email': user1['email']}).json()
    assert len(res['fans']) == 1
    assert res['fans'][0]['email'] == user2['email']
    res = client.get("/getStarsByEmail", params={'email': user2['email']}).json()
    assert len(res['stars']) == 1
    assert res['stars'][0]['email'] == user1['email']

    res = (client.post("/searchUserAPage",
                      json={'searchContent':mock_user_data['username'][2:-4],
                            'pageno':1,
                            'pagesize':1,
                            'nowSortMethod':'byTime'}
                       ).json()
           )
    assert res['userSum'] == 2
    res = (client.post("/searchUserAPage",
                       json={'searchContent': '6666',
                             'pageno': 1,
                             'pagesize': 100,
                             'nowSortMethod': 'byTime'}
                       ).json()
           )
    assert res['userSum'] == 1
    res = (client.post("/searchUserAPage",
                       json={'searchContent': '123',
                             'pageno': 1,
                             'pagesize': 100,
                             'nowSortMethod': 'byTime'}
                       ).json()
           )
    assert res['userSum'] == 1


def test_set_sign(mock_user_data, new_database):
    register_login_user(client, mock_user_data)
    res = client.put("/logout")
    res = client.post("/setSignByEmail", json={'email':mock_user_data['email'], 'sign':"testsign"})
    assert res.status_code == 400
    res = client.put("/login", json=mock_user_data)
    res = client.post("/setSignByEmail", json={'email': mock_user_data['email'], 'sign': "testsign"})
    assert res.status_code == 200
    client.put('/logout')
    res = client.get("/getInfoByEmail",params={'email':mock_user_data['email']})
    assert res.json()['sign'] == 'testsign'

def test_set_nickname(mock_user_data, new_database):
    register_login_user(client, mock_user_data)
    client.put('/logout')
    res = client.post('/setNicknameByEmail',
                      json={'email':mock_user_data['email'], 'nickname':"testnickname"})
    assert res.status_code == 400
    res = client.put('/login', json=mock_user_data)
    res = client.post('/setNicknameByEmail',
                      json={'email': mock_user_data['email'], 'nickname': "testnickname"})
    assert res.status_code == 200
    res = client.get("/getInfoByEmail", params={'email': mock_user_data['email']})
    assert res.json()['nickname'] == 'testnickname'

def test_set_head_url(mock_user_data, new_database):
    register_login_user(client, mock_user_data)
    client.post("/setHeadImageByEmail", json={'email':mock_user_data['email'],
                                              'url':"http://newavator.url"})
    res = client.get("/getInfoByEmail", params={'email': mock_user_data['email']}).json()
    assert res['url'] == 'http://newavator.url'