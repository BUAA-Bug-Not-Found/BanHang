from datetime import datetime

from fastapi import APIRouter, Depends, Header, Query, BackgroundTasks
from sqlalchemy.orm import Session
from orm.database import get_db
import orm.schemas as schemas
import orm.crud as crud
from pydantic import BaseModel
from tools.check_user import check_user, authorize
from typing import List, Optional, Union
from banhang.user import successResponse, excResponse
from banhang.BanHangException import UniException

router = APIRouter()


class QuestionContent(BaseModel):
    content: str
    imageList: List[str]


class GetQuestionsResponse(BaseModel):
    # quesId,userId,userName,
    # quesContent,quesState,quesTime,
    # ifUserLike, ansSum, likeSum,
    # tagIdList
    quesId: int
    userId: int
    userName: str
    quesContent: QuestionContent
    quesState: int
    quesTime: datetime
    ifUserLike: bool
    ansSum: int
    likeSum: int
    tagIdList: List[int]
    ifUserFocus:bool


class GetQuestionsNewResponse(BaseModel):
    questions: List[GetQuestionsResponse]
    quesSum: int


@router.get("/getQuestions", tags=["Question"], response_model=GetQuestionsNewResponse,
            responses={400: {"model": excResponse}})
def get_questions_by_page(pageNo: int = Query(..., description="页面号，从 1 开始计数"),
                          pageSize: int = Query(..., description="每页问题数量"),
                          db: Session = Depends(get_db),
                          current_user: Optional[dict] = Depends(authorize)):
    """
    imageList保存image的url
    """
    if pageNo <= 0 or pageSize <= 0:
        raise UniException(key="isSuccess", value=False,
                           others={"description": "pageNo或pageSize小于等于零，不符合要求。"})
    offset = (pageNo - 1) * pageSize
    limit = pageSize
    db_questions = list(crud.get_questions(db, offset=offset, limit=limit, asc=False,
                                           input_user_id=current_user['uid'] if current_user else 0))
    qids = [q.question_id for q in db_questions]
    questions_tags = crud.get_questions_tags(db, qids)
    questions_images = crud.get_questions_images_urls(db, qids)
    questions = []
    for question in db_questions:
        # quesId,userId,userName,
        # quesContent,quesState,quesTime,
        # ifUserLike, ansSum, likeSum,
        # tagIdList
        retquestion = {}
        retquestion['quesId'] = question.question_id
        retquestion['userId'] = question.user_id
        retquestion['userName'] = question.user_name
        retquestion['quesContent'] = {'content': question.question_content,
                                      'imageList': questions_images[question.question_id]}
        retquestion['quesState'] = 0 if question.question_delated else \
            1 if question.question_archived else \
                2 if not question.question_solved else \
                    3
        retquestion['quesTime'] = question.question_create_at
        retquestion['ifUserLike'] = question.if_user_like
        retquestion['ansSum'] = question.ans_sum
        retquestion['likeSum'] = question.like_sum
        retquestion['tagIdList'] = questions_tags[question.question_id]
        retquestion['ifUserFocus'] = question.if_user_focus
        questions.append(retquestion)
    return {"questions": questions, "quesSum": crud.get_question_num(db)}


@router.get("/getQuestionsByTagId", tags=["Question"], response_model=GetQuestionsNewResponse,
            responses={400: {"model": excResponse}})
def get_questions_by_tag_id(pageNo: int = Query(..., description="页面号，从 1 开始计数"),
                          pageSize: int = Query(..., description="每页问题数量"),
                            tagId: int = Query(..., description="标签id"),
                          db: Session = Depends(get_db),
                          current_user: Optional[dict] = Depends(authorize)):
    """
    imageList保存image的url
    """
    if pageNo <= 0 or pageSize <= 0:
        raise UniException(key="isSuccess", value=False,
                           others={"description": "pageNo或pageSize小于等于零，不符合要求。"})
    alltag = crud.get_all_question_tags(db)
    tagid_tag_map = {}
    for tag in alltag:
        tagid_tag_map[tag.id] = tag
    if not tagId in tagid_tag_map:
        raise UniException(key="isSuccess", value=False,
                           others={"description": "标签不存在。"})
    offset = (pageNo - 1) * pageSize
    limit = pageSize
    db_questions = crud.get_questions_by_tag(db, offset=offset, limit=limit, asc=False, tag = tagid_tag_map[tagId],
                                             input_user_id=current_user['uid'] if current_user else 0)

    qids = [q.question_id for q in db_questions]
    questions_tags = crud.get_questions_tags(db, qids)
    questions_images = crud.get_questions_images_urls(db, qids)
    questions = []
    for question in db_questions:
        # quesId,userId,userName,
        # quesContent,quesState,quesTime,
        # ifUserLike, ansSum, likeSum,
        # tagIdList
        retquestion = {}
        retquestion['quesId'] = question.question_id
        retquestion['userId'] = question.user_id
        retquestion['userName'] = question.user_name
        retquestion['quesContent'] = {'content': question.question_content,
                                      'imageList': questions_images[question.question_id]}
        retquestion['quesState'] = 0 if question.question_delated else \
            1 if question.question_archived else \
                2 if not question.question_solved else \
                    3
        retquestion['quesTime'] = question.question_create_at
        retquestion['ifUserLike'] = question.if_user_like
        retquestion['ansSum'] = question.ans_sum
        retquestion['likeSum'] = question.like_sum
        retquestion['tagIdList'] = questions_tags[question.question_id]
        retquestion['ifUserFocus'] = question.if_user_focus
        questions.append(retquestion)
    return {"questions": questions, "quesSum": crud.get_question_sum_by_tag_id(db, tagId)}


class QuestionContent(BaseModel):
    content: str
    imageList: List[str]


class UploadQuestion(BaseModel):
    quesContent: QuestionContent
    quesTags: Union[List[str], List[int]]


def check_question_tag_to_id(tags: Union[List[str], List[int]], db):
    if len(tags) > 0:
        if type(tags[0]) is int:
            alltags = set([t.id for t in crud.get_all_question_tags(db)])
            for tag in tags:
                if tag not in alltags:
                    raise UniException(key="isSuccess", value=False,
                                       others={"description": "包含不存在的tagid，可以尝试直接传入tag名，后端会自动创建"})
        else:
            tagid = []
            for tag in tags:
                if not crud.get_question_tag_by_name(db, tag):
                    tagid.append(crud.create_question_tag(db, tag).id)
            tags.clear()
            for tag in tagid:
                tags.append(tag)


def check_question_image_to_id(images: List[str], db, questionId: int):
    retimage = []
    for url in images:
        if image := crud.get_question_image_by_url(db, url):
            retimage.append(image.id)
        else:
            image = crud.create_question_image(db, schemas.QuestionImageCreate(questionId=questionId,
                                                                               imageUrl=url))
            retimage.append(image.id)
    images.clear()
    for id in retimage:
        images.append(id)


@router.post('/uploadQues', tags=["Question"], response_model=successResponse,
             responses={400: {"model": excResponse}})
def upload_question(question: UploadQuestion, db: Session = Depends(get_db),
                    current_user: Optional[dict] = Depends(authorize)):
    """
        imageList保存image的url
    """
    if not current_user:
        raise UniException(key="isSuccess", value=False, others={"description": "用户未登录"})
    tagid = question.quesTags
    check_question_tag_to_id(tagid, db)
    created_ques = crud.create_question(db, schemas.QuestionCreate(content=question.quesContent.content,
                                                                   userId=current_user["uid"],
                                                                   questionTagids=tagid,
                                                                   questionImageids=[]))

    check_question_image_to_id(question.quesContent.imageList, db, created_ques.id)
    crud.update_question(db, created_ques.id, schemas.QuestionCreate(content=question.quesContent.content,
                                                                     userId=current_user["uid"],
                                                                     questionTagids=tagid,
                                                                     questionImageids=question.quesContent.imageList))
    return {"isSuccess": True}


class UpdateQuestion(UploadQuestion):
    quesId: int


@router.post("/updateQues", tags=["Question"], response_model=successResponse,
             responses={400: {"model": excResponse}})
def update_question(question: UpdateQuestion, db: Session = Depends(get_db),
                    current_user: Optional[dict] = Depends(authorize)):
    """
        imageList保存image的url
    """
    ques = crud.get_question_by_id(db, question.quesId)
    user = crud.get_user_by_id(db, current_user["uid"])
    if not ques:
        raise UniException(key="isSuccess", value=False, others={"description": "不存在该id的问题"})
    if user.privilege == 0 and current_user['uid'] != ques.user_id:
        raise UniException(key="isSuccess", value=False, others={"description": "用户无权更新该问题"})

    check_question_tag_to_id(question.quesTags, db)
    check_question_image_to_id(question.quesContent.imageList, db, question.quesId)

    crud.update_question(db, question.quesId, schemas.QuestionCreate(content=question.quesContent.content,
                                                                     userId=current_user["uid"],
                                                                     questionTagids=question.quesTags,
                                                                     questionImageids=question.quesContent.imageList))
    return {"isSuccess": True}


class AnsContent(BaseModel):
    content: str
    imageList: List[str]


class AnsQuestion(BaseModel):
    quesId: int
    ansContent: AnsContent


def check_question_comment_image_to_id(images: List[str], db, questionCommentId: int):
    retimage = []
    for url in images:
        if image := crud.get_question_comment_image_by_url(db, url):
            retimage.append(image.id)
        else:
            image = crud.create_question_comment_image(db, schemas.QuestionCommentImageCreate(
                questionCommentId=questionCommentId,
                imageUrl=url))
            retimage.append(image.id)
    images.clear()
    for id in retimage:
        images.append(id)


class UpdateAnswer(BaseModel):
    ansId: int
    ansContent: AnsContent


@router.post("/answerQues", tags=["Question"], response_model=successResponse,
             responses={400: {"model": excResponse}})
def answer_question(ans: AnsQuestion, background_tasks: BackgroundTasks, db: Session = Depends(get_db),
                    current_user: Optional[dict] = Depends(authorize)):
    if not current_user:
        raise UniException(key="isSuccess", value=False, others={"description": "用户未登录"})
    if not crud.get_question_by_id(db, ans.quesId):
        raise UniException(key="isSuccess", value=False, others={"description": "问题id不存在"})
    comment = crud.create_question_comment(db, schemas.QuestionCommentCreat(
        content=ans.ansContent.content,
        userId=current_user['uid'],
        questionCommentImageids=[],
        questionId=ans.quesId
    ), background_tasks)
    check_question_comment_image_to_id(ans.ansContent.imageList, db, comment.id)
    comment = crud.update_question_comment(db, comment.id, schemas.QuestionCommentCreat(
        content=ans.ansContent.content,
        userId=current_user['uid'],
        questionCommentImageids=ans.ansContent.imageList,
        questionId=ans.quesId
    ))
    return {"isSuccess": True}

class ReplyAnswerRequest(BaseModel):
    replyCommentId: int
    ansContent: AnsContent

@router.post("/replyComment", tags=["Question"], response_model=successResponse)
def reply_comment(ans_req:ReplyAnswerRequest, background_tasks: BackgroundTasks,
                              db: Session = Depends(get_db), current_user: Optional[dict] = Depends(authorize)):
    if not current_user:
        raise UniException(key="isSuccess", value=False, others={"description": "用户未登录"})
    target_comment = crud.get_question_comment_by_id(db, ans_req.replyCommentId)
    if not target_comment:
        raise UniException(key="isSuccess", value=False, others={"description": "回答id不存在"})
    # target_question = target_comment.question
    comment = crud.create_question_comment(db, schemas.QuestionCommentCreat(
        content=ans_req.ansContent.content,
        userId=current_user['uid'],
        questionCommentImageids=[],
        questionId=target_comment.question_id,
        replyCommentId=target_comment.id
    ), background_tasks)
    check_question_comment_image_to_id(ans_req.ansContent.imageList, db, comment.id)
    comment = crud.update_question_comment(db, comment.id, schemas.QuestionCommentCreat(
        content=ans_req.ansContent.content,
        userId=current_user['uid'],
        questionCommentImageids=[],
        questionId=target_comment.question_id,
        replyCommentId=target_comment.id
    ))
    return successResponse()



@router.post("/updateAns", tags=["Question"], response_model=successResponse,
             responses={400: {"model": excResponse}})
def update_answer(update_ans: UpdateAnswer, db: Session = Depends(get_db),
                    current_user: Optional[dict] = Depends(authorize)):
    if not current_user:
        raise UniException(key="isSuccess", value=False, others={"description": "用户未登录"})
    if not crud.get_question_comment_by_id(db, update_ans.ansId):
        raise UniException(key="isSuccess", value=False, others={"description": "回答id不存在"})
    if crud.get_question_comment_by_id(db, update_ans.ansId).user_id != current_user['uid'] and \
            crud.get_user_by_id(db, current_user['uid']).privilege == 0:
        raise UniException(key="isSuccess", value=False, others={"description": "该用户无权限更改该回答"})
    check_question_comment_image_to_id(update_ans.ansContent.imageList, db, update_ans.ansId)
    comment = crud.update_question_comment(db, update_ans.ansId, schemas.QuestionCommentCreat(
        content=update_ans.ansContent.content,
        userId=current_user['uid'],
        questionCommentImageids=update_ans.ansContent.imageList
    ))
    return {"isSuccess": True}


class setAnsType(BaseModel):
    ansId: int
    setType: int


@router.post("/setAnsType", tags=["Question"], response_model=successResponse,
             responses={400: {"model": excResponse}})
def set_answer_accept(ansTypeSet: setAnsType, db: Session = Depends(get_db),
                      current_user: Optional[dict] = Depends(authorize)):
    accept = ansTypeSet.setType == 1
    ansId = ansTypeSet.ansId
    if not current_user:
        raise UniException(key="isSuccess", value=False, others={"description": "用户未登录"})
    if not crud.get_question_comment_by_id(db, ansId):
        raise UniException(key="isSuccess", value=False, others={"description": "回答id不存在"})
    if crud.get_question_comment_by_id(db, ansId).user_id != current_user['uid'] and \
            crud.get_user_by_id(db, current_user['uid']).privilege == 0:
        raise UniException(key="isSuccess", value=False, others={"description": "该用户无权限更改该回答采纳状态"})
    crud.set_ans_accept(db, accept, ansId)
    return {"isSuccess": True}


class setLikeQuestion(BaseModel):
    setType: int
    quesId: int


class setLikeAnswer(BaseModel):
    setType: int
    ansId: int


@router.post("/setLikeQues", tags=["Question"], response_model=successResponse,
             responses={400: {"model": excResponse}})
def set_question_like(set_like_ques: setLikeQuestion, background_tasks: BackgroundTasks, db: Session = Depends(get_db),
                      current_user: Optional[dict] = Depends(authorize)):
    like = set_like_ques.setType == 1
    quesId = set_like_ques.quesId
    if not current_user:
        raise UniException(key="isSuccess", value=False, others={"description": "用户未登录"})
    if not crud.get_question_by_id(db, quesId):
        raise UniException(key="isSuccess", value=False, others={"description": "问题不存在"})
    crud.set_like_question(db, current_user['uid'], quesId, like, background_tasks)
    return {"isSuccess": True}

class SetFocusQuestionRequest(BaseModel):
    quesId:int
    ifFocus:int
@router.post("/setFocusQues", tags=["Question"], response_model=successResponse,
             responses={400: {"model": excResponse}})
def set_question_focus(set_focus_ques: SetFocusQuestionRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db),
                      current_user: Optional[dict] = Depends(authorize)):
    focus = set_focus_ques.ifFocus == 1
    quesId = set_focus_ques.quesId
    if not current_user:
        raise UniException(key="isSuccess", value=False, others={"description": "用户未登录"})
    if not crud.get_question_by_id(db, quesId):
        raise UniException(key="isSuccess", value=False, others={"description": "问题不存在"})
    crud.set_focus_question(db, current_user['uid'], quesId, focus, background_tasks)
    return {"isSuccess": True}


@router.post("/setLikeAns", tags=["Question"], response_model=successResponse,
             responses={400: {"model": excResponse}})
def set_answer_like(set_like_answer: setLikeAnswer, background_tasks: BackgroundTasks, db: Session = Depends(get_db),
                    current_user: Optional[dict] = Depends(authorize)):
    like = set_like_answer.setType == 1
    ansId = set_like_answer.ansId
    if not current_user:
        raise UniException(key="isSuccess", value=False, others={"description": "用户未登录"})
    if not crud.get_question_comment_by_id(db, ansId):
        raise UniException(key="isSuccess", value=False, others={"description": "回答不存在"})
    crud.set_like_question_comment(db, current_user['uid'], ansId, like, background_tasks)
    return {"isSuccess": True}


class QuestionResponse(BaseModel):
    userId: int
    userName: str
    quesContent: QuestionContent
    quesState: int
    quesTime: datetime
    ifUserLike: bool
    likeSum: int
    tagIdList: List[int]
    ansIdList: List[int]
    ifUserFocus: bool


class GetQuestionResponse(BaseModel):
    ifExist: bool
    question: Optional[QuestionResponse]


@router.get("/getQuesById", tags=["Question"], response_model=GetQuestionResponse)
def get_question_by_id(quesId: int, db: Session = Depends(get_db),
                       current_user: Optional[dict] = Depends(authorize)):
    question = crud.get_question_by_id(db, quesId)
    if not question:
        return {"ifExist": False, "question": None}
    question_response = QuestionResponse(
        userId=question.user_id,
        userName=crud.get_user_by_id(db, question.user_id).username,
        quesContent={'content':question.content, 'imageList':[image.image_url for image in question.images]},
        quesState=0 if question.delated else 1 if question.archived else 2 if not question.solved else 3,
        quesTime=question.create_at,
        ifUserLike=current_user is not None and question in crud.get_user_by_id(db, current_user['uid']).liked_questions,
        likeSum=len(question.liked_users),
        tagIdList=[tag.id for tag in question.tags],
        ansIdList=[ans.id for ans in question.comments],
        ifUserFocus=current_user is not None and question in crud.get_user_by_id(db, current_user['uid']).focused_questions
    )

    return {"ifExist": True, "question": question_response}


class QuestionAnswerResponse(BaseModel):
    userId: int
    userName: str
    ansContent: str
    ansState: int
    ansTime: datetime
    ifUserLike: bool
    likeSum: int
    replyAnsId: int


class GetQuestionAnswerResponse(BaseModel):
    ifExist: bool
    answer: Optional[QuestionAnswerResponse]


@router.get("/getAnsById", tags=["Question"], response_model=GetQuestionAnswerResponse)
def get_question_answer_by_id(ansId: int, db: Session = Depends(get_db),
                              current_user: Optional[dict] = Depends(authorize)):
    answer = crud.get_question_comment_by_id(db, ansId)
    if not answer:
        return {"ifExist": False, "answer": None}
    question_answer_response = QuestionAnswerResponse(
        userId=answer.user_id,
        userName=crud.get_user_by_id(db, answer.user_id).username,
        ansContent=answer.content,
        ansState=0 if answer.delated else 1 if not answer.accepted else 2,
        ansTime=answer.create_at,
        ifUserLike=current_user is not None and answer in crud.get_user_by_id(db, current_user['uid']).liked_question_comments,
        likeSum=len(answer.liked_users),
        replyAnsId=answer.reply_comment_id if answer.reply_comment_id else -1
    )

    return {"ifExist": True, "answer": question_answer_response}



class TagResponse(BaseModel):
    tagId: int
    tagName: str
    tagIcon: str
    tagColor: str


class GetTagsResponse(BaseModel):
    tags: List[TagResponse]


@router.get("/getTags", tags=["Question"], response_model=GetTagsResponse)
def get_tags(db: Session = Depends(get_db)):
    return {'tags': [{'tagId': tag.id,
                      'tagName': tag.name,
                      'tagIcon': tag.icon,
                      'tagColor': tag.color} for tag in crud.get_question_tag_all(db)
                     ]}

class SearchQuestionsRequest(BaseModel):
    searchContent:str
    pageno:int
    pagesize:int
    nowSortMethod:str

@router.post("/searchQuesAPage", tags=["Question"], response_model=GetQuestionsNewResponse)
def search_questions_by_content(search_questions_request:SearchQuestionsRequest,db: Session = Depends(get_db),
                      current_user: Optional[dict] = Depends(authorize)):
    try:
        sort_mode = {'byRelation':1, 'byTime':2, 'byPopularity':3}[search_questions_request.nowSortMethod]
    except:
        raise UniException(key="isSuccess", value=False,
                           others={"description": "nowSortMethod参数错误，请检查。"})
    wordlist = [x.strip() for x in search_questions_request.searchContent.split(" ") if x != ""]
    pageNo = search_questions_request.pageno
    pageSize = search_questions_request.pagesize
    if pageNo <= 0 or pageSize <= 0:
        raise UniException(key="isSuccess", value=False,
                           others={"description": "pageNo或pageSize小于等于零，不符合要求。"})
    offset = (pageNo - 1) * pageSize
    limit = pageSize
    db_questions= crud.search_question_by_word_list(db, wordlist, offset=offset, limit=limit, asc=sort_mode)
    questions = []
    current_user = crud.get_user_by_id(db, current_user["uid"]) if current_user else None
    for question in db_questions:
        # quesId,userId,userName,
        # quesContent,quesState,quesTime,
        # ifUserLike, ansSum, likeSum,
        # tagIdList
        user = question.user
        retquestion = {}
        retquestion['quesId'] = question.id
        retquestion['userId'] = user.id
        retquestion['userName'] = user.username
        retquestion['quesContent'] = {'content': question.content,
                                      'imageList': [image.image_url for image in question.images]}
        retquestion['quesState'] = 0 if question.delated else \
            1 if question.archived else \
                2 if not question.solved else \
                    3
        retquestion['quesTime'] = question.create_at
        retquestion['ifUserLike'] = (
            current_user in question.liked_users if current_user else False)
        retquestion['ansSum'] = len(question.comments)
        retquestion['likeSum'] = len(question.liked_users)
        retquestion['tagIdList'] = [tag.id for tag in question.tags]
        retquestion['ifUserFocus'] = (
            current_user in question.focused_users if current_user else False
        )
        questions.append(retquestion)
    return {"questions": questions,
            "quesSum": crud.get_search_question_sum_by_word_list(db, wordlist, offset=offset, limit=limit, asc=2)}


class QuestionIdRequest(BaseModel):
    quesId: int
@router.post("/delQuestion", tags=["Question"], response_model=successResponse)
def del_question(req: QuestionIdRequest, db: Session = Depends(get_db),
                 current_user: Optional[dict] = Depends(authorize)):
    question = crud.get_question_by_id(db, req.quesId)
    if not question:
        raise UniException(key="isSuccess", value=False,
                           others={"description": "questionId不存在，请检查。"})
    if question.user_id != current_user['uid'] and crud.get_user_by_id(db, current_user['uid']).privilege==0:
        raise UniException(key="isSuccess", value=False,
                           others={"description": "用户无权限"})
    crud.delete_question_by_id(db, req.quesId)
    return successResponse()

class AnswerIdRequest(BaseModel):
    ansId: int
@router.post("/delAnswer", tags=["Question"], response_model=successResponse)
def del_answer(req: AnswerIdRequest, db: Session = Depends(get_db),
                 current_user: Optional[dict] = Depends(authorize)):
    if not current_user:
        raise UniException(key="isSuccess", value=False,
                           others={"description": "用户未登录，请先登录。"})
    comment = crud.get_question_comment_by_id(db, req.ansId)
    if not comment:
        raise UniException(key="isSuccess", value=False,
                           others={"description": "ansId不存在，请检查。"})
    if comment.user_id != current_user['uid'] and crud.get_user_by_id(db, current_user['uid']).privilege==0:
        raise UniException(key="isSuccess", value=False,
                           others={"description": "用户无权限"})
    crud.delete_question_comment_by_id(db, req.ansId)
    return successResponse()

@router.post("/solveQuestion", tags=["Question"], response_model=successResponse)
def solve_question(req: QuestionIdRequest, db: Session = Depends(get_db),
                   current_user: Optional[dict] = Depends(authorize)):
    if not current_user:
        raise UniException(key="isSuccess", value=False,
                           others={"description": "用户未登录，请先登录。"})
    question = crud.get_question_by_id(db, req.quesId)
    if not question:
        raise UniException(key="isSuccess", value=False, others={"description": "questionId不存在。"})
    if question.user_id != current_user['uid'] and crud.get_user_by_id(db, current_user['uid']).privilege==0:
        raise UniException(key="isSuccess", value=False,
                           others={"description": "用户无权限"})
    crud.set_question_solved(db, req.quesId)
    return successResponse()