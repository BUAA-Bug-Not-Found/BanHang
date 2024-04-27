import pytest
from prepare import *
# 一定写在前面


from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_upload(mock_blog_data, mock_user_data, new_database):
    # 注册登录
    os.environ["CHECKCODE"] = mock_user_data["checkCode"]
    client.post("/sendCheckCode", json={"email": mock_user_data["email"]})
    res = client.post("/registerUser", json=mock_user_data)
    res = client.put("/login", json=mock_user_data)
    user_info = client.get("check_login_state").json()
    assert res.status_code == 200
    # 发送消息
    res = client.post("/sendMessage", json={"targetUserId": user_info["uid"], "content": "Hello world!"}).json()
    assert res['status'] == "success"
    res = client.post("/getHistoryMessage",json = {"targetUserId": user_info["uid"]}).json()
    assert len(res) == 1
    print(res)