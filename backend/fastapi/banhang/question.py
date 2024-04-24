from datetime import datetime

from fastapi import APIRouter, Depends, Header, Query
from sqlalchemy.orm import Session
from orm.database import get_db
import orm.schemas as schemas
import orm.crud as crud
from pydantic import BaseModel
from tools.check_user import check_user, authorize
from typing import List, Optional, Union
from banhang.user import successResponse
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


@router.get("/getQuestions", tags=["Question"], response_model=List[GetQuestionsResponse])
def get_questions_by_page(pageNo: int = Query(..., description="页面号，从 1 开始计数"),
                          pageSize: int = Query(..., description="每页问题数量"),
                          db: Session = Depends(get_db),
                          current_user: Optional[dict] = Depends(authorize)):
    if pageNo <= 0 or pageSize <= 0:
        raise UniException(key="isSuccess", value=False, others={"description": "pageNo或pageSize小于等于零，不符合要求。"})
    offset = (PageNo - 1) * PageSize
    limit = PageSize
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
    return questions


class QuestionContent(BaseModel):
    content: str
    imageList: List[int]


class UploadQuestion(BaseModel):
    quesContent: QuestionContent
    quesTags: Union[List[str], List[int]]


@router.post('/uploadQues', tags=["Question"], response_model=successResponse)
def upload_question(question: UploadQuestion, db: Session = Depends(get_db),
                    current_user: Optional[dict] = Depends(authorize)):
    if not current_user:
        raise UniException(key="isSuccess", value=False, others={"description": "用户未登录"})
    tagid = question.quesTags
    if len(question.quesTags) > 0:
        if type(question.quesTags[0]) is int:
            alltags = set(crud.get_all_question_tags(db))
            for tag in question.quesTags:
                if tag not in alltags:
                    raise UniException(key="isSuccess", value=False,
                                       others={"description": "包含不存在的tagid，可以尝试直接传入tag名，后端会自动创建"})
        else:
            tagid = []
            for tag in question.quesTags:
                if not crud.get_question_tag_by_name(db, tag):
                    tagid.append(crud.create_question_tag(db, tag).id)
    image_entities = [crud.get_question_image_by_id(imageid) for imageid in question.quesContent.imageList]
    if None in image_entities:
        raise UniException(key="isSuccess", value=False, others={"description": "包含不存在的imageid"})
    crud.create_question(db, schemas.QuestionCreate(content=question.quesContent.content,
                                                    userId=current_user["uid"],
                                                    questionTagids=tagid,
                                                    questionImageids=question.quesContent.imageList))
    return {"isSuccess": True}
