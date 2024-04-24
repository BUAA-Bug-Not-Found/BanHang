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
    


