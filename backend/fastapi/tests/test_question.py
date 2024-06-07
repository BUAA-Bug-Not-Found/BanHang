import time
from typing import List

from prepare import *
# 一定写在前面


from fastapi.testclient import TestClient
from main import app

from tests.test_user import register_login_user

client = TestClient(app)


def add_tags(tagnames: List[str]):
    i = 0
    ret = True
    for name in tagnames:
        i += 1
        res = client.post("/addQuestionTag", json={'name': name, 'id': i, 'color': "a", 'icon': 'b',
                                                   'isAdmin': False})
        ret = ret and (res.status_code == 200)
    return ret


def test_upload(mock_question_data, mock_user_data, new_database, mock_question_comment_data):
    # 注册登录
    register_login_user(client, mock_user_data, admin=True)
    add_tags(mock_question_data['quesTags'])

    # 上传blog
    res = client.post("/uploadQues", json=mock_question_data)
    assert res.status_code == 200
    # 检查blog是否存在
    blogs = client.get("/getQuestions", params={"pageNo": 1, "pageSize": 100}).json()
    assert len(blogs["questions"]) == 1
    assert blogs["questions"][0]["userName"] == mock_user_data['username']
    assert blogs["questions"][0]['quesContent']['content'] == mock_question_data["quesContent"]['content']
    idlist = blogs["questions"][0]['tagIdList']

    blogs = client.get('/getQuestionsByTagId', params={"pageNo": 1, "pageSize": 100, 'tagId': idlist[0]}).json()
    assert len(blogs["questions"]) == 1
    assert blogs["questions"][0]["userName"] == mock_user_data['username']
    assert blogs["questions"][0]['quesContent']['content'] == mock_question_data["quesContent"]['content']

    # 测试update问题
    mock_question_data["quesContent"]["content"] = "changed content"
    mock_question_data['quesId'] = blogs['questions'][0]['quesId']
    res = client.post("/updateQues", json=mock_question_data)
    assert res.status_code == 200

    # 检查update后的问题
    blogs = client.get("/getQuestions", params={"pageNo": 1, "pageSize": 100}).json()
    assert len(blogs["questions"]) == 1
    blog = blogs['questions'][0]
    assert blog["userName"] == mock_user_data['username']
    assert blog['quesContent']['content'] == mock_question_data["quesContent"]['content']
    assert blog["quesContent"]['imageList'] == mock_question_data["quesContent"]["imageList"]
    mock_user_2 = mock_user_data.copy()
    mock_user_2['email'] = "test2@buaa.edu.cn"

    # 检查用户权限
    register_login_user(client, mock_user_2)
    mock_question_data["quesContent"]["content"] = "changed content2"
    res = client.post("/updateQues", json=mock_question_data)
    assert res.status_code != 200

    register_login_user(client, mock_user_data)

    mock_question_comment_data['quesId'] = blogs['questions'][0]['quesId']
    # 尝试comment
    res = client.post("/answerQues", json=mock_question_comment_data)
    assert res.status_code == 200
    ans = client.get("/getQuesById", params={"quesId": blog["quesId"]}).json()
    assert ans["ifExist"] == True
    assert len(ans['question']['ansIdList']) == 1
    answerid = ans['question']['ansIdList'][0]

    ans1 = client.get('/getAnsById', params={"ansId": answerid}).json()
    assert ans1["ifExist"] == True
    assert ans1['answer']['ansContent'] == mock_question_comment_data['ansContent']['content']

    # 尝试like ques
    res = client.post("/setLikeQues", json={'quesId': blog['quesId'], 'setType': 1})
    assert res.status_code == 200
    ans = client.get("/getQuesById", params={"quesId": blog["quesId"]}).json()
    assert ans["ifExist"] == True
    assert ans["question"]['ifUserLike'] == True
    assert ans["question"]['likeSum'] == 1

    # 尝试focus ques
    res = client.post("/setFocusQues", json={'quesId': blog['quesId'], 'ifFocus': 1})
    assert res.status_code == 200
    ans = client.get("/getQuesById", params={"quesId": blog["quesId"]}).json()
    assert ans["ifExist"] == True
    assert ans["question"]['ifUserFocus'] == True

    # 尝试like comment
    res = client.post("/setLikeAns", json={'ansId': answerid, 'setType': 1})
    assert res.status_code == 200
    ans1 = client.get('/getAnsById', params={"ansId": answerid}).json()
    assert ans1["ifExist"] == True
    assert ans1['answer']['ifUserLike'] == True
    assert ans1['answer']['likeSum'] == 1

    # update answers
    mock_question_comment_data['ansContent']['content'] = "changed content"
    mock_question_comment_data['ansId'] = answerid
    res = client.post("/updateAns", json=mock_question_comment_data)
    assert res.status_code == 200
    ans1 = client.get('/getAnsById', params={"ansId": answerid}).json()
    assert ans1["ifExist"] == True
    assert ans1['answer']['ansContent'] == mock_question_comment_data['ansContent']['content']

    # accept answers
    res = client.post("/setAnsType", json={'ansId': answerid, 'setType': 1})
    assert res.status_code == 200
    ans1 = client.get('/getAnsById', params={"ansId": answerid}).json()
    assert ans1["ifExist"] == True
    assert ans1['answer']['ansState'] == 2
    ans = client.get("/getQuesById", params={"quesId": blog["quesId"]}).json()
    assert ans["ifExist"] == True
    assert ans["question"]["quesState"] == 3

    time.sleep(1)
    mock_question_data["quesContent"]['content'] = "new question content"
    res = client.post("/uploadQues", json=mock_question_data)
    assert res.status_code == 200
    # 检查blog是否存在
    blogs = client.get("/getQuestions", params={"pageNo": 1, "pageSize": 100}).json()
    assert len(blogs["questions"]) == 2
    assert blogs["questions"][0]["userName"] == mock_user_data['username']
    assert blogs["questions"][0]['quesContent']['content'] == mock_question_data["quesContent"]['content']

    blogs = client.post("/searchQuesAPage", json={'searchContent': "new", 'pageno': 1, 'pagesize': 100,
                                                  'nowSortMethod': 'byTime'})
    assert blogs.status_code == 200
    assert blogs.json()['quesSum'] == 1
    assert blogs.json()['questions'][0]['quesContent']['content'] == mock_question_data["quesContent"]['content']


def test_delete_question_and_comment(mock_question_data, mock_user_data, new_database, mock_question_comment_data):
    # 注册登录
    register_login_user(client, mock_user_data, admin=True)
    add_tags(mock_question_data['quesTags'])
    # 上传blog
    res = client.post("/uploadQues", json=mock_question_data)
    assert res.status_code == 200
    # 检查blog是否存在
    blogs = client.get("/getQuestions", params={"pageNo": 1, "pageSize": 100}).json()
    assert len(blogs["questions"]) == 1
    assert blogs["questions"][0]["userName"] == mock_user_data['username']
    assert blogs["questions"][0]['quesContent']['content'] == mock_question_data["quesContent"]['content']
    idlist = blogs["questions"][0]['tagIdList']

    res = client.post("/delQuestion", json={"quesId": blogs['questions'][0]['quesId']})
    blogs = client.get("/getQuestions", params={"pageNo": 1, "pageSize": 100}).json()
    assert len(blogs["questions"]) == 0

    # 重新上传
    res = client.post("/uploadQues", json=mock_question_data)
    assert res.status_code == 200
    blogs = client.get("/getQuestions", params={"pageNo": 1, "pageSize": 100}).json()
    assert len(blogs["questions"]) == 1
    # answer
    mock_question_comment_data['quesId'] = blogs['questions'][0]['quesId']
    res = client.post("/answerQues", json=mock_question_comment_data)
    assert res.status_code == 200
    ans = client.get("/getQuesById", params={"quesId": blogs['questions'][0]["quesId"]}).json()
    assert ans["ifExist"] == True
    assert len(ans['question']['ansIdList']) == 1
    answerid = ans['question']['ansIdList'][0]

    # delete answer_id
    res = client.post("/delAnswer", json={"ansId": answerid})
    ans = client.get("/getQuesById", params={"quesId": blogs['questions'][0]["quesId"]}).json()
    assert ans["ifExist"] == True
    assert len(ans['question']['ansIdList']) == 0


def test_solved_question(mock_question_data, mock_user_data, new_database, mock_question_comment_data):
    # 注册登录
    register_login_user(client, mock_user_data, admin=True)
    add_tags(mock_question_data['quesTags'])
    # 上传blog
    res = client.post("/uploadQues", json=mock_question_data)
    assert res.status_code == 200
    # 检查blog是否存在
    blogs = client.get("/getQuestions", params={"pageNo": 1, "pageSize": 100}).json()
    assert len(blogs["questions"]) == 1
    assert blogs["questions"][0]["userName"] == mock_user_data['username']
    assert blogs["questions"][0]['quesContent']['content'] == mock_question_data["quesContent"]['content']

    # 标记问题solved
    res = client.post('/solveQuestion', json={'quesId': blogs['questions'][0]['quesId']})
    assert res.status_code == 200

    # 检查是否解决
    blogs = client.get("/getQuestions", params={"pageNo": 1, "pageSize": 100}).json()
    assert len(blogs["questions"]) == 1
    assert blogs["questions"][0]["quesState"] == 3


def test_comment_to_comment(mock_question_data, mock_user_data, new_database, mock_question_comment_data):
    # 注册登录
    register_login_user(client, mock_user_data, admin=True)
    add_tags(mock_question_data['quesTags'])
    # 上传blog
    res = client.post("/uploadQues", json=mock_question_data)
    assert res.status_code == 200
    # 检查blog是否存在
    blogs = client.get("/getQuestions", params={"pageNo": 1, "pageSize": 100}).json()
    assert len(blogs["questions"]) == 1
    assert blogs["questions"][0]["userName"] == mock_user_data['username']
    assert blogs["questions"][0]['quesContent']['content'] == mock_question_data["quesContent"]['content']
    idlist = blogs["questions"][0]['tagIdList']

    blogs = client.get('/getQuestionsByTagId', params={"pageNo": 1, "pageSize": 100, 'tagId': idlist[0]}).json()
    assert len(blogs["questions"]) == 1
    assert blogs["questions"][0]["userName"] == mock_user_data['username']
    assert blogs["questions"][0]['quesContent']['content'] == mock_question_data["quesContent"]['content']
    blog = blogs['questions'][0]

    mock_question_comment_data['quesId'] = blogs['questions'][0]['quesId']
    # 尝试comment
    res = client.post("/answerQues", json=mock_question_comment_data)
    assert res.status_code == 200
    ans = client.get("/getQuesById", params={"quesId": blog["quesId"]}).json()
    assert ans["ifExist"] == True
    assert len(ans['question']['ansIdList']) == 1
    answerid = ans['question']['ansIdList'][0]

    ans1 = client.get('/getAnsById', params={"ansId": answerid}).json()
    assert ans1["ifExist"] == True
    assert ans1['answer']['ansContent'] == mock_question_comment_data['ansContent']['content']

    # 尝试comment comment
    mock_question_comment_data['replyCommentId'] = answerid
    mock_question_comment_data['ansContent']['content'] = "hahaha"
    res = client.post('/replyComment', json=mock_question_comment_data)
    assert res.status_code == 200

    ques = client.get("/getQuesById", params={"quesId": blog["quesId"]}).json()
    assert ques["ifExist"] == True
    assert len(ques['question']['ansIdList']) == 1
    top_ans = ques['question']['ansIdList'][0]
    top_ans = client.get('/getAnsById', params={"ansId": top_ans}).json()
    assert top_ans['ifExist'] == True
    assert len(top_ans['answer']['subAnsIdList']) == 1
    sub_ans_id1 = top_ans['answer']['subAnsIdList'][0]

    ans1 = client.get('/getAnsById', params={"ansId": sub_ans_id1}).json()
    assert ans1["ifExist"] == True
    assert ans1['answer']['ansContent'] == mock_question_comment_data['ansContent']['content']
    assert ans1['answer']['replyAnsId'] == answerid

    time.sleep(1)
    # 尝试comment comment comment
    mock_question_comment_data['replyCommentId'] = sub_ans_id1
    mock_question_comment_data['ansContent']['content'] = "hahaha2"
    res = client.post('/replyComment', json=mock_question_comment_data)
    assert res.status_code == 200

    ques = client.get("/getQuesById", params={"quesId": blog["quesId"]}).json()
    assert ques["ifExist"] == True
    assert len(ques['question']['ansIdList']) == 1
    top_ans = ques['question']['ansIdList'][0]
    top_ans = client.get('/getAnsById', params={"ansId": top_ans}).json()
    assert top_ans['ifExist'] == True
    assert len(top_ans['answer']['subAnsIdList']) == 2
    sub_ans_id2 = top_ans['answer']['subAnsIdList'][1]

    ans2 = client.get('/getAnsById', params={"ansId": sub_ans_id2}).json()
    assert ans2["ifExist"] == True
    assert ans2['answer']['ansContent'] == mock_question_comment_data['ansContent']['content']
    assert ans2['answer']['replyAnsId'] == sub_ans_id1


def test_create_question_tag_by_nonAdmin(mock_question_data, mock_user_data, new_database, mock_question_comment_data):
    # 注册登录
    register_login_user(client, mock_user_data, admin=False)
    ret = add_tags(mock_question_data['quesTags'])
    assert ret == False


def test_report_question(mock_question_data, mock_user_data, new_database):
    register_login_user(client, mock_user_data, admin=True)
    uid1 = client.get("check_login_state").json()['uid']
    ret = add_tags(mock_question_data['quesTags'])
    assert ret == True

    # 上传一个question并检查存在性
    res = client.post("/uploadQues", json=mock_question_data)
    assert res.status_code == 200
    blogs = client.get("/getQuestions", params={"pageNo": 1, "pageSize": 100}).json()
    assert len(blogs["questions"]) == 1
    assert blogs["questions"][0]["userName"] == mock_user_data['username']
    assert blogs["questions"][0]['quesContent']['content'] == mock_question_data["quesContent"]['content']
    quesid = blogs["questions"][0]['quesId']

    mock_user_2 = mock_user_data.copy()
    mock_user_2['email'] = "test2@buaa.edu.cn"
    register_login_user(client, mock_user_2, admin=False)
    # 举报

    ret = client.post('/reportQues', json={'quesId': quesid, 'reportReason': "这个问题有问题"})
    assert ret.status_code == 200
    # 非管理员获取举报数据
    ret1 = client.get('/getComplainAmount')
    assert ret1.status_code == 400
    # 管理员获取举报数据
    register_login_user(client, mock_user_data, admin=True)
    ret1 = client.get('/getComplainAmount')
    assert ret1.status_code == 200
    assert ret1.json()['count'] == 1

    issues = client.get("/getComplainList").json()
    assert len(issues) == 1
    issue = issues[0]
    assert issue['isAno'] == False
    assert issue['isComment'] == False
    assert issue['blogContent'] == mock_question_data['quesContent']['content']
    assert issue['blogAuthorId'] == uid1
    assert issue['cause'] == '这个问题有问题'


def test_report_question_comment(mock_question_data, mock_user_data, mock_question_comment_data, new_database):
    register_login_user(client, mock_user_data, admin=True)
    uid1 = client.get("check_login_state").json()['uid']
    ret = add_tags(mock_question_data['quesTags'])
    assert ret == True

    # 上传一个question并检查存在性
    res = client.post("/uploadQues", json=mock_question_data)
    assert res.status_code == 200
    blogs = client.get("/getQuestions", params={"pageNo": 1, "pageSize": 100}).json()
    assert len(blogs["questions"]) == 1
    assert blogs["questions"][0]["userName"] == mock_user_data['username']
    assert blogs["questions"][0]['quesContent']['content'] == mock_question_data["quesContent"]['content']
    quesid = blogs["questions"][0]['quesId']

    mock_question_comment_data['quesId'] = quesid
    # 尝试comment
    res = client.post("/answerQues", json=mock_question_comment_data)
    assert res.status_code == 200
    ans = client.get("/getQuesById", params={"quesId": quesid}).json()
    assert ans["ifExist"] == True
    assert len(ans['question']['ansIdList']) == 1
    answerid = ans['question']['ansIdList'][0]

    mock_user_2 = mock_user_data.copy()
    mock_user_2['email'] = "test2@buaa.edu.cn"
    register_login_user(client, mock_user_2, admin=False)
    # 举报
    ret = client.post('/reportAnswer', json={'quesId': quesid, 'ansId': answerid, 'reportReason': "这个问题有问题"})
    assert ret.status_code == 200
    # 非管理员获取举报数据
    ret1 = client.get('/getComplainAmount')
    assert ret1.status_code == 400
    # 管理员获取举报数据
    register_login_user(client, mock_user_data, admin=True)
    ret1 = client.get('/getComplainAmount')
    assert ret1.status_code == 200
    assert ret1.json()['count'] == 1

    issues = client.get("/getComplainList").json()
    assert len(issues) == 1
    issue = issues[0]
    assert issue['isAno'] == False
    assert issue['isComment'] == True
    assert issue['blogContent'] == mock_question_data['quesContent']['content']
    assert issue['comment'] == mock_question_comment_data['ansContent']['content']
    assert issue['blogAuthorId'] == uid1
    assert issue['commentAuthorId'] == uid1
    assert issue['cause'] == '这个问题有问题'
    issue_id = issue['complainId']

    # 尝试删除该issue
    ret = client.post('/deleteComplainItem', json={'id': issue_id})
    assert ret.status_code == 200
    ret1 = client.get('/getComplainAmount')
    assert ret1.status_code == 200
    assert ret1.json()['count'] == 0


def test_shutup_user(mock_question_data, mock_user_data, mock_question_comment_data, new_database):
    register_login_user(client, mock_user_data, admin=False)
    uid1 = client.get("check_login_state").json()['uid']

    mock_user_2 = mock_user_data.copy()
    mock_user_2['email'] = "test2@buaa.edu.cn"
    register_login_user(client, mock_user_2, admin=True)
    uid2 = client.get("check_login_state").json()['uid']
    ret = add_tags(mock_question_data['quesTags'])
    assert ret == True

    # 禁言用户1
    ret = client.post('/shutUpUser', json={'id': uid1, 'day': 1, 'hour': 1, 'min': 1})
    assert ret.status_code == 200
    # 检查用户1是否被禁言
    ret = client.post('/isShutUpByUserId', json={'id': uid1})
    assert ret.status_code == 200
    assert ret.json()['isShutUp'] == True

    # 检查用户1是否能够发表言论
    register_login_user(client, mock_user_data, admin=False)
    res = client.post("/uploadQues", json=mock_question_data)
    assert res.status_code == 400

    # 检查非管理员能否查看禁言状态
    ret = client.post('/isShutUpByUserId', json={'id': uid1})
    assert ret.status_code == 200
