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
    # 上传blog
    res = client.post("/blog/uploadBlog", json = mock_blog_data)
    assert res.status_code == 200
    # 检查blog是否存在
    blogs = client.post("/blog/getBlogs",json = {"nowTag":-1, "pageno": 1,"pagesize": 100}).json()
    assert len(blogs) == 1
    assert blogs[0]["title"] == mock_blog_data["title"]
    assert blogs[0]["content"] == mock_blog_data["content"]
    assert blogs[0]["userId"] == user_info["uid"]

