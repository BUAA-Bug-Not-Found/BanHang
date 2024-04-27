from datetime import datetime

from fastapi import APIRouter, Depends, Header, Query
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

class GetQuestionNewResponse(BaseModel):
    questions:List[GetQuestionsResponse]
    quesSum:int



@router.get("/getQuestions", tags=["Question"], response_model=GetQuestionNewResponse,
            responses={400: {"model": excResponse}})
def get_questions_by_page(pageNo: int = Query(..., description="页面号，从 1 开始计数"),
                          pageSize: int = Query(..., description="每页问题数量"),
                          db: Session = Depends(get_db),
                          current_user: Optional[dict] = Depends(authorize)):
    """
    imageList保存image的url
    """
    if pageNo <= 0 or pageSize <= 0:
        raise UniException(key="isSuccess", value=False, others={"description": "pageNo或pageSize小于等于零，不符合要求。"})
    offset = (pageNo - 1) * pageSize
    limit = pageSize
    db_questions = crud.get_questions(db, offset=offset, limit=limit, asc=False)
    questions = []
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
            crud.get_user_by_id(db, current_user["uid"]) in question.liked_users if current_user else
            False)
        retquestion['ansSum'] = len(question.comments)
        retquestion['likeSum'] = len(question.liked_users)
        retquestion['tagIdList'] = [tag.id for tag in question.tags]
        questions.append(retquestion)
    return {"questions":questions, "quesSum":crud.get_question_num(db)}


class QuestionContent(BaseModel):
    content: str
    imageList: List[str]


class UploadQuestion(BaseModel):
    quesContent: QuestionContent
    quesTags: Union[List[str], List[int]]

def check_question_tag_to_id(tags:Union[List[str], List[int]], db):
    if len(tags) > 0:
        if type(tags[0]) is int:
            alltags = set(crud.get_all_question_tags(db))
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

def check_question_image_to_id(images:List[str], db, questionId:int):
    retimage = []
    for url in images:
        if image:=crud.get_question_image_by_url(db, url):
            retimage.append(image.id)
        else:
            image = crud.create_question_image(db, schemas.QuestionImageCreate(questionId = questionId,
                                                                               imageUrl = url))
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
def update_question(question:UpdateQuestion, db:Session = Depends(get_db),
                    current_user: Optional[dict] = Depends(authorize)):
    """
        imageList保存image的url
    """
    ques = crud.get_question_by_id(db, question.quesId)
    user = crud.get_user_by_id(db, current_user["uid"])
    if not ques:
        return UniException(key="isSuccess", value=False, others={"description": "不存在该id的问题"})
    if user.privilege == 0 and current_user['uid']!= ques.user_id:
        return UniException(key="isSuccess", value=False, others={"description":"用户无权更新该问题"})

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

def check_question_comment_image_to_id(images:List[str], db, questionCommentId:int):
    retimage = []
    for url in images:
        if image:=crud.get_question_comment_image_by_url(db, url):
            retimage.append(image.id)
        else:
            image = crud.create_question_comment_image(db, schemas.QuestionCommentImageCreate(
                questionCommentId = questionCommentId,
                imageUrl = url))
            retimage.append(image.id)
    images.clear()
    for id in retimage:
        images.append(id)

@router.post("/answerQues", tags=["Question"], response_model=successResponse,
             responses={400: {"model": excResponse}})
def update_question(ans:AnsQuestion, db:Session = Depends(get_db),
                    current_user: Optional[dict] = Depends(authorize)):
    if not current_user:
        return UniException(key="isSuccess", value=False, others={"description": "用户未登录"})
    if not crud.get_question_by_id(db, ans.quesId):
        return UniException(key="isSuccess", value=False, others={"description": "问题id不存在"})
    comment = crud.create_question_comment(db, schemas.QuestionCommentCreat(
        content=ans.ansContent.content,
        userId = current_user['uid'],
        questionCommentImageids = [],
        questionId = ans.quesId
    ))
    check_question_comment_image_to_id(ans.ansContent.imageList, db, comment.id)
    comment = crud.update_question_comment(db, comment.id, schemas.QuestionCommentCreat(
        content=ans.ansContent.content,
        userId = current_user['uid'],
        questionCommentImageids = ans.ansContent.imageList,
        questionId = ans.quesId
    ))
    return {"isSuccess": True}

