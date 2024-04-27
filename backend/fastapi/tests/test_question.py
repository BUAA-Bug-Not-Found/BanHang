import pytest
from prepare import *
# 一定写在前面


from fastapi.testclient import TestClient
from main import app

from tests.test_user import register_login_user

client = TestClient(app)

def test_upload(mock_question_data, mock_user_data, new_database, mock_question_comment_data):
    # 注册登录
    register_login_user(client, mock_user_data)
    # 上传blog
    res = client.post("/uploadQues", json = mock_question_data)
    assert res.status_code == 200
    # 检查blog是否存在
    blogs = client.get("/getQuestions",params = {"pageNo": 1,"pageSize": 100}).json()
    assert len(blogs["questions"]) == 1
    assert blogs["questions"][0]["userName"] == mock_user_data['username']
    assert blogs["questions"][0]['quesContent']['content'] == mock_question_data["quesContent"]['content']

    # 测试update问题
    mock_question_data["quesContent"]["content"] = "changed content"
    mock_question_data['quesId'] = blogs['questions'][0]['quesId']
    res = client.post("/updateQues", json = mock_question_data)
    assert res.status_code == 200

    # 检查update后的问题
    blogs = client.get("/getQuestions", params={"pageNo": 1, "pageSize": 100}).json()
    assert len(blogs["questions"]) == 1
    blog = blogs['questions'][0]
    assert blog["userName"] == mock_user_data['username']
    assert blog['quesContent']['content'] == mock_question_data["quesContent"]['content']
    assert blog["quesContent"]['imageList'] == mock_question_data["quesContent"]["imageList"]

    mock_question_comment_data['quesId'] = blogs['questions'][0]['quesId']
    # 尝试comment
    res = client.post("/answerQues", json = mock_question_comment_data)
    assert res.status_code == 200
    ans = client.get("/getQuesById", params={"quesId": blog["quesId"]}).json()
    assert ans["ifExist"] == True
    assert len(ans['question']['ansIdList']) == 1
    answerid = ans['question']['ansIdList'][0]

    ans1 = client.get('/getAnsById', params={"ansId": answerid}).json()
    assert ans1["ifExist"] == True
    assert ans1['answer']['ansContent'] == mock_question_comment_data['ansContent']['content']

    # 尝试like ques
    res = client.post("/setLikeQues", json = {'quesId': blog['quesId'], 'setType': 1})
    assert res.status_code == 200
    ans = client.get("/getQuesById", params={"quesId": blog["quesId"]}).json()
    assert ans["ifExist"] == True
    assert ans["question"]['ifUserLike'] == True
    assert ans["question"]['likeSum'] == 1

    # 尝试like comment
    res = client.post("/setLikeAns", json = {'ansId': answerid, 'setType': 1})
    assert res.status_code == 200
    ans1 = client.get('/getAnsById', params={"ansId": answerid}).json()
    assert ans1["ifExist"] == True
    assert ans1['answer']['ifUserLike'] == True
    assert ans1['answer']['likeSum'] == 1

    # update answers
    mock_question_comment_data['ansContent']['content'] = "changed content"
    mock_question_comment_data['ansId'] = answerid
    res = client.post("/updateAns", json = mock_question_comment_data)
    assert res.status_code == 200
    ans1 = client.get('/getAnsById', params={"ansId": answerid}).json()
    assert ans1["ifExist"] == True
    assert ans1['answer']['ansContent'] == mock_question_comment_data['ansContent']['content']

    # accept answers
    res = client.post("/setAnsType", json = {'ansId': answerid, 'setType': 1})
    assert res.status_code == 200
    ans1 = client.get('/getAnsById', params={"ansId": answerid}).json()
    assert ans1["ifExist"] == True
    assert ans1['answer']['ansState'] == 2
    ans = client.get("/getQuesById", params={"quesId": blog["quesId"]}).json()
    assert ans["ifExist"] == True
    assert ans["question"]["quesState"] == 3


