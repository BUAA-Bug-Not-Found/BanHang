import pytest
from prepare import *
# 一定写在前面


from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# 后文出现的该函数名会自动被pytest调用该函数并传入测试用例

def register_login_user(client, mock_user_data, admin=False):
    if admin:
        os.environ["BANHANG_TEST_ADMIN"] = 'True'
    else:
        os.environ["BANHANG_TEST_ADMIN"] = 'False'
    os.environ["CHECKCODE"] = mock_user_data["checkCode"]
    client.post("/sendCheckCode", json={"email": mock_user_data["email"]})
    client.post("/registerUser", json=mock_user_data)
    response = client.put("/login", json=mock_user_data)
    assert response.status_code == 200


def test_register_success(mock_user_data, new_database):
    os.environ["CHECKCODE"] = mock_user_data["checkCode"]
    client.post("/sendCheckCode", json={"email": mock_user_data["email"]})
    # 测试用户注册成功的情况
    response = client.post("/registerUser", json=mock_user_data)
    assert response.status_code == 200
    assert response.json() == {"isSuccess": True}


def test_register_failure(mock_user_data, new_database):
    os.environ["CHECKCODE"] = mock_user_data["checkCode"]
    client.post("/sendCheckCode", json={"email": mock_user_data["email"]})
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
    mock_user_data["email"] = "123" + mock_user_data["email"]
    mock_user_data['username'] += '6666'
    register_login_user(client, mock_user_data)
    user2 = client.get("check_login_state").json()
    assert user2['email'] == mock_user_data["email"]
    res = client.get("/queryStarById", params={"id1": user2["uid"], "id2": user1["uid"]}).json()
    assert res['isStar'] == False
    client.post("/setStarStateById", json={'id1': user2['uid'], 'id2': user1['uid'],
                                           'state': True})
    res = client.get("/queryStarById", params={"id1": user2["uid"], "id2": user1["uid"]}).json()
    assert res['isStar'] == True
    res = client.get("/getFansById", params={'id': user1['uid']}).json()
    assert len(res['fans']) == 1
    assert res['fans'][0]['id'] == user2['uid']
    res = client.get("/getStarsById", params={'id': user2['uid']}).json()
    assert len(res['stars']) == 1
    assert res['stars'][0]['id'] == user1['uid']

    res = (client.post("/searchUserAPage",
                       json={'searchContent': mock_user_data['username'][2:-4],
                             'pageno': 1,
                             'pagesize': 1,
                             'nowSortMethod': 'byTime'}
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
    user = client.get("check_login_state").json()
    res = client.put("/logout")
    res = client.post("/setSignById", json={'id': user['uid'], 'sign': "testsign"})
    assert res.status_code == 400
    res = client.put("/login", json=mock_user_data)
    res = client.post("/setSignById", json={'id': user['uid'], 'sign': "testsign"})
    assert res.status_code == 200
    client.put('/logout')
    res = client.get("/getOtherInfosById", params={'id': user['uid']})
    assert res.json()['sign'] == 'testsign'


def test_set_nickname(mock_user_data, new_database):
    register_login_user(client, mock_user_data)
    user = client.get("check_login_state").json()
    client.put('/logout')
    res = client.post('/setNicknameById',
                      json={'id': user['uid'], 'nickname': "testnickname"})
    assert res.status_code == 400
    res = client.put('/login', json=mock_user_data)
    res = client.post('/setNicknameById',
                      json={'id': user['uid'], 'nickname': "testnickname"})
    assert res.status_code == 200
    res = client.get("/getOtherInfosById", params={'id': user['uid']})
    assert res.json()['nickname'] == 'testnickname'


def test_set_head_url(mock_user_data, new_database):
    register_login_user(client, mock_user_data)
    user = client.get("check_login_state").json()
    client.post("/setHeadImageById", json={'id': user['uid'],
                                           'url': "http://newavator.url"})
    res = client.get("/getOtherInfosById", params={'id': user['uid']}).json()
    assert res['url'] == 'http://newavator.url'


def test_original_exp(mock_user_data, new_database):
    register_login_user(client, mock_user_data)
    user = client.get("check_login_state").json()
    user_id = user['uid']
    levelreq = client.post('/getCurrentLevelById', json={'id': user_id})
    assert levelreq.status_code == 200
    assert levelreq.json()['level'] == 0
    expreq = client.post('/getCurrentExpById', json={'id': user_id})
    assert expreq.status_code == 200
    assert expreq.json()['exp'] == 0
