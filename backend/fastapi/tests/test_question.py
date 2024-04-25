import pytest
from prepare import *
# 一定写在前面


from fastapi.testclient import TestClient
from main import app

from tests.test_user import register_login_user

client = TestClient(app)

def test_upload(mock_question_data, mock_user_data, new_database):
    # 注册登录
    register_login_user(client, mock_user_data)
    # 上传blog
    res = client.post("/uploadQues", json = mock_question_data)
    assert res.status_code == 200
    # 检查blog是否存在
    blogs = client.get("/getQuestions",params = {"pageNo": 1,"pageSize": 100}).json()
    assert len(blogs) == 1
    assert blogs[0]["userName"] == mock_user_data['username']
    assert blogs[0]['quesContent']['content'] == mock_question_data["quesContent"]['content']

