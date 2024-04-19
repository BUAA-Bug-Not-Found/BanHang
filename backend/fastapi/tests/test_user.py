import pytest
import prepare
# 一定写在前面
from prepare import mock_user_data, new_database


from fastapi.testclient import TestClient
from backend.fastapi.main import app

client = TestClient(app)
# 后文出现的该函数名会自动被pytest调用该函数并传入测试用例


def test_register_success(mock_user_data, new_database):
    # 测试用户注册成功的情况
    response = client.put("/banhang/register", json=mock_user_data)
    assert response.status_code == 200
    assert response.json() == {"response": "success"}

def test_register_failure(mock_user_data, new_database):
    # 测试用户注册失败的情况（用户已存在）
    client.put("/banhang/register", json=mock_user_data)  # 首次注册应该成功
    response = client.put("/banhang/register", json=mock_user_data)  # 重复注册应该失败
    assert response.status_code == 400
    assert response.json() == {"detail": "user exists"}

def test_login(mock_user_data):
    # 测试用户登录成功的情况
    response = client.put("/banhang/login", json=mock_user_data)
    assert response.status_code == 200
    assert "token" in response.json()

def test_login_failure(mock_user_data):
    # 测试用户登录失败的情况
    wrong_data = {
        "username": mock_user_data["username"],
        "password": "wrongpassword"
    }
    response = client.put("/banhang/login", json=wrong_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid username or password"}
