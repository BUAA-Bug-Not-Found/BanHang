import os
import re
from datetime import datetime
from typing import Optional, List
import hashlib
from scripts.buaa_api_renewer import data as vacant_data

from fastapi import Depends, FastAPI, HTTPException, APIRouter, Response, Cookie, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy.sql.functions import user

from orm import crud, schemas
from orm.database import get_db

from tools.check_user import generate_jwt_token, authorize, check_user
from tools.mail import MailSender, is_valid_email
import banhang.BanHangException as EXC
import random

router = APIRouter()


# Dependency


class successResponse(BaseModel):
    isSuccess: bool = True


class loginRequest(BaseModel):
    email: str
    password: str


class usernameRequest(BaseModel):
    username: str


class emailRequest(BaseModel):
    email: str


class registerRequest(schemas.UserCreate):
    checkCode: str


class resetPasswordRequest(loginRequest):
    checkCode: str


class userResponse(BaseModel):
    username: str
    email: str
    uid: int


class excResponse(BaseModel):
    isSuccess: bool = False
    discription: str


def checkNickname(nickname: str) -> bool:
    r = '^[0-9a-zA-Z-_\u4e00-\u9fa5]*$'
    result = re.match(r, nickname)
    return result is not None


def update_password_to_hash(password: str) -> str:
    return hashlib.sha256((password + "banhang").encode()).hexdigest()


class LoginResponse(BaseModel):
    isSuccess: bool = True
    id: int


@router.put("/login", tags=["注册登录"], response_model=LoginResponse,
            responses={400: {"model": excResponse}})
def login(req: loginRequest, request: Request, response: Response, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, req.email)
    if not user or (user.password != req.password and update_password_to_hash(req.password) != user.password):
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "Invalid username or password",
                                                                     'id': 0})
    if not req.email.endswith("buaa.edu.cn"):
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "邮箱不是北航邮箱，目前仅北航使用"})
    response.set_cookie(key="Auth", value=generate_jwt_token(user.id, user.username),
                        samesite='none',
                        secure=False if os.environ.get("CHECKCODE") is not None else True)
    return {"isSuccess": True, 'id': user.id}


@router.put("/logout", tags=["注册登录"], response_model=successResponse,
            responses={400: {"model": excResponse}})
def logout(response: Response):
    response.set_cookie(key="Auth", value="logout")
    return {"isSuccess": True}


@router.post("/registerUser", tags=["注册登录"], response_model=successResponse,
             responses={400: {"model": excResponse}})
def register(req: registerRequest, db: Session = Depends(get_db)):
    if not crud.is_valid_checkCode(db, req.checkCode, req.email):
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "Invalid check"})
    if not req.email.endswith("buaa.edu.cn"):
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "邮箱不是北航邮箱，目前仅北航使用"})
    user = crud.get_user_by_email(db, req.email)
    if user:
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "user exists"})
    if not checkNickname(req.username):
        raise EXC.UniException(key="isSuccess", value=False,
                               others={"description": "用户名不符合要求，只允许包含中文、字母、数字、英文下划线和连字符"})
    crud.create_user(db, schemas.UserCreate(username=req.username, password=update_password_to_hash(req.password),
                                            email=req.email))
    return {"isSuccess": True}


@router.get("/check_login_state", tags=["注册登录"], response_model=userResponse,
            responses={400: {"model": excResponse}})
def check_login_state(current_user: Optional[dict] = Depends(authorize), db: Session = Depends(get_db)):
    if current_user:
        current_user["email"] = crud.get_user_by_id(db, current_user["uid"]).email
        return current_user
    raise EXC.UniException(key="isSuccess", value=False, others={"description": "user not login"})


@router.post("/sendCheckCode", tags=["注册登录"], response_model=successResponse,
             responses={400: {"model": excResponse}})
def send_check_code(req: emailRequest, db: Session = Depends(get_db)):
    checkcode = random.choice(range(10000, 100000))
    # print(checkcode)
    if os.environ.get("CHECKCODE") is not None:
        checkcode = int(os.environ.get("CHECKCODE"))
    if not is_valid_email(req.email):
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "invalid email"})
    if not req.email.endswith("buaa.edu.cn"):
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "邮箱不是北航邮箱，目前仅北航使用"})
    try:
        if os.environ.get("CHECKCODE") is None:
            MailSender.send_by_buaa_mail(req.email, checkcode)
            pass
        crud.create_checkcode_record(db, schemas.EmailCheck(email=req.email, checkcode=checkcode))
        return {"isSuccess": True}
    except:
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "内部错误"})


@router.post("/resetPassword", tags=["注册登录"], response_model=successResponse,
             responses={400: {"model": excResponse}})
def reset_password(req: resetPasswordRequest, db: Session = Depends(get_db)):
    if not crud.is_valid_checkCode(db, req.checkCode, req.email):
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "Invalid check"})
    if not req.email.endswith("buaa.edu.cn"):
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "邮箱不是北航邮箱，目前仅北航使用"})
    user = crud.get_user_by_email(db, req.email)
    if not user:
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "用户不存在"})
    crud.set_password_by_email(db, update_password_to_hash(req.password), req.email)
    return {"response": "success"}


class UserInfoResponse(BaseModel):
    nickname: str
    sign: str
    url: str
    user_id: int
    email: str


@router.get("/getCurrentUserInfo", tags=['用户中心'], response_model=UserInfoResponse,
            responses={400: {"model": excResponse}})
def get_current_user_info(current_user: Optional[dict] = Depends(authorize), db: Session = Depends(get_db)):
    if not current_user:
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "用户未登录"})
    user = crud.get_user_by_id(db, current_user['uid'])
    if not user:
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "用户不存在"})
    return {"nickname": user.username, "sign": user.sign, 'url': user.userAvatarURL if user.userAvatarURL else "",
            'user_id': user.id, 'email': user.email}


class SetSignRequestNew(BaseModel):
    id: int
    sign: str


@router.post("/setSignById", tags=['用户中心'], response_model=successResponse,
             responses={400: {"model": excResponse}})
def set_sign_by_id(req: SetSignRequestNew, current_user: Optional[dict] = Depends(authorize),
                   db: Session = Depends(get_db)):
    if not current_user:
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "用户未登录"})
    user = crud.get_user_by_id(db, req.id)
    current_user_instance = crud.get_user_by_id(db, current_user['uid'])
    if current_user_instance.privilege == 0 and current_user_instance.email != user.email:
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "用户无权限"})
    user = crud.set_sign_by_id(db, req.id, req.sign)
    return successResponse()


class SetNicknameRequestNew(BaseModel):
    id: int
    nickname: str


@router.post("/setNicknameById", tags=['用户中心'], response_model=successResponse,
             responses={400: {"model": excResponse}})
def set_nickname_by_id(req: SetNicknameRequestNew, current_user: Optional[dict] = Depends(authorize),
                       db: Session = Depends(get_db)):
    if not current_user:
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "用户未登录"})
    user = crud.get_user_by_id(db, req.id)
    current_user_instance = crud.get_user_by_id(db, current_user['uid'])
    if current_user_instance.privilege == 0 and current_user_instance.email != user.email:
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "用户无权限"})
    if not checkNickname(req.nickname):
        raise EXC.UniException(key="isSuccess", value=False,
                               others={"description": "用户名不符合要求，只允许包含中文、字母、数字、英文下划线和连字符"})
    user = crud.set_username_by_id(db, req.id, req.nickname)
    return successResponse()


class GetAnonyBlogResponse(BaseModel):
    blogTitle: str
    firstPhotoUrl: str
    time: datetime
    blogId: int
    blogText: str


@router.get("/getAnonyBlogsById", tags=['用户中心'], response_model=List[GetAnonyBlogResponse],
            responses={400: {"model": excResponse}})
def get_anonyBlogs_by_id(id: int, current_user: Optional[dict] = Depends(authorize),
                         db: Session = Depends(get_db)):
    if not current_user:
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "用户未登录"})
    user = crud.get_user_by_id(db, id)
    current_user_instance = crud.get_user_by_id(db, current_user['uid'])
    if current_user_instance.privilege == 0 and current_user_instance.email != user.email:
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "用户无权限"})
    blogs = crud.get_blogs_by_user_id(db, id, not_deleted=True)
    return [GetAnonyBlogResponse(blogTitle=blog.title,
                                 firstPhotoUrl=blog.images[0].image_url if len(blog.images) > 0 else "",
                                 time=blog.create_at,
                                 blogId=blog.id,
                                 blogText=blog.content)
            for blog in blogs]


class GetHelpBlogResponse(BaseModel):
    blogTitle: str
    firstPhotoUrl: str
    time: datetime
    blogId: int


@router.get("/getHelpBlogsById", tags=['用户中心'], response_model=List[GetHelpBlogResponse],
            responses={400: {"model": excResponse}})
def get_helpBlogs_by_id(id: int,  # current_user: Optional[dict] = Depends(authorize),
                        db: Session = Depends(get_db)):
    # if not current_user:
    #     pass
    #     # raise EXC.UniException(key = "isSuccess", value=False, others={"description":"用户未登录"})
    # user = crud.get_user_by_email(db, email)
    # current_user_instance = crud.get_user_by_id(db, current_user['uid'])
    # if current_user_instance.privilege == 0 and current_user_instance.email != user.email:
    #     pass
    #     # raise EXC.UniException(key = "isSuccess", value=False, others={"description":"用户无权限"})
    questions = crud.get_questions_by_user_id(db, id)
    return [GetHelpBlogResponse(blogTitle=question.content,
                                firstPhotoUrl=question.images[0].image_url if len(question.images) > 0 else "",
                                time=question.create_at,
                                blogId=question.id)
            for question in questions]


class QueryStarResponse(BaseModel):
    isStar: bool


@router.get("/queryStarById", tags=["用户中心"], response_model=QueryStarResponse,
            responses={400: {"model": excResponse}})
def query_star_by_id(id1: int, id2: int, db: Session = Depends(get_db)):
    user1 = crud.get_user_by_id(db, id1)
    user2 = crud.get_user_by_id(db, id2)
    if not user1 or not user2:
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "用户不存在"})
    return {"isStar": user2 in user1.followed}


class SetStarRequestNew(BaseModel):
    id1: int
    id2: int
    state: bool


@router.post("/setStarStateById", response_model=successResponse, tags=["用户中心"],
             responses={400: {"model": excResponse}})
def set_star_state_by_id(req: SetStarRequestNew, db: Session = Depends(get_db),
                         current_user: Optional[dict] = Depends(authorize)):
    current_user_isntance = crud.get_user_by_id(db, current_user['uid'])
    user1 = crud.get_user_by_id(db, req.id1)
    user2 = crud.get_user_by_id(db, req.id2)
    if not user1 or not user2:
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "用户不存在"})
    if current_user_isntance.privilege == 0 and current_user_isntance.email != user1.email:
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "无权修改别人的follow状态"})
    crud.set_star_state_by_user_id(db, req.id1, req.id2, is_followed=req.state)
    return successResponse()


class UserResponse(BaseModel):
    nickname: str
    sign: str
    url: str
    id: int


class UserSearchResponse(BaseModel):
    users: List[UserResponse]
    userSum: int


class SearchUsersRequest(BaseModel):
    searchContent: str
    pageno: int
    pagesize: int
    nowSortMethod: str


@router.post("/searchUserAPage", tags=["用户中心"], response_model=UserSearchResponse)
def search_questions_by_content(req: SearchUsersRequest, db: Session = Depends(get_db),
                                current_user: Optional[dict] = Depends(authorize)):
    # try:
    #     sort_mode = {'byRelation':1, 'byTime':2, 'byPopularity':3}[search_questions_request.nowSortMethod]
    # except:
    #     raise EXC.UniException(key="isSuccess", value=False,
    #                        others={"description": "nowSortMethod参数错误，请检查。"})
    # wordlist = [x.strip() for x in search_questions_request.searchContent.split(" ") if x != ""]
    pageNo = req.pageno
    pageSize = req.pagesize
    if pageNo <= 0 or pageSize <= 0:
        raise EXC.UniException(key="isSuccess", value=False,
                               others={"description": "pageNo或pageSize小于等于零，不符合要求。"})
    offset = (pageNo - 1) * pageSize
    limit = pageSize
    db_users = crud.search_user_by_word(db, req.searchContent, offset=offset, limit=limit)
    users = [{'nickname': user.username, 'sign': user.sign, 'url': user.userAvatarURL if user.userAvatarURL else "",
              'email': user.email, 'id': user.id}
             for user in db_users]
    return {"users": users,
            "userSum": crud.get_search_user_sum_by_word(db, req.searchContent, offset=offset, limit=limit)}


class FansResponseNew(BaseModel):
    id: int
    headUrl: str
    nickname: str
    sign: str


class getFansResponseNew(BaseModel):
    fans: List[FansResponseNew]


@router.get("/getFansById", tags=['用户中心'], response_model=getFansResponseNew)
def get_fans_by_id(id: int, db: Session = Depends(get_db),
                   current_user: Optional[dict] = Depends(authorize)):
    user = crud.get_user_by_id(db, id)
    if user is None:
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "用户不存在"})
    fans = [{'id': fan.id, 'headUrl': fan.userAvatarURL, 'nickname': fan.username, 'sign': fan.sign}
            for fan in user.followers]
    return {'fans': fans}


class getStarsResponseNew(BaseModel):
    stars: List[FansResponseNew]


@router.get("/getStarsById", tags=['用户中心'], response_model=getStarsResponseNew)
def get_stars_by_id(id: int, db: Session = Depends(get_db),
                    current_user: Optional[dict] = Depends(authorize)):
    user = crud.get_user_by_id(db, id)
    if user is None:
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "用户不存在"})
    stars = [{'id': star.id, 'headUrl': star.userAvatarURL, 'nickname': star.username, 'sign': star.sign}
             for star in user.followed]
    return {'stars': stars}


class SetUserHeadUrlRequestNew(BaseModel):
    url: str
    id: int


@router.post("/setHeadImageById", tags=['用户中心'], response_model=successResponse)
def set_head_image_by_id(req: SetUserHeadUrlRequestNew, db: Session = Depends(get_db),
                         current_user: Optional[dict] = Depends(authorize)):
    if not current_user:
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "请登录"})
    user = crud.get_user_by_id(db, req.id)
    cur_user = crud.get_user_by_id(db, current_user['uid'])
    if user is None or (req.id != cur_user.id and cur_user.privilege == 0):
        raise EXC.UniException(key="isSuccess", value=False,
                               others={"description": "用户不存在" if not user else "用户无权限"})
    crud.set_user_head_url_by_id(db, req.id, req.url)
    return successResponse()


class OtherUserInfoResponse(BaseModel):
    nickname: str
    sign: str
    url: str
    isManager: bool


@router.get("/getOtherInfosById", tags=['用户中心'], response_model=OtherUserInfoResponse,
            responses={400: {"model": excResponse}})
def get_other_info_by_id(id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, id)
    if not user:
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "用户不存在"})
    return {"nickname": user.username, "sign": user.sign, 'url': user.userAvatarURL if user.userAvatarURL else "",
            'isManager': user.privilege > 0}


@router.get("/getInfoByUserId", tags=['用户中心'], response_model=UserInfoResponse, deprecated=True,  # todo deprecated
            responses={400: {"model": excResponse}})
def get_info_by_id(userId: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, userId)
    if not user:
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "用户不存在"})
    return {"nickname": user.username, "sign": user.sign, 'url': user.userAvatarURL if user.userAvatarURL else "",
            'user_id': user.id, 'email': 'anonymous'}


class vacantClassroomInfo(BaseModel):
    name: str
    vacant_time: List[int]


class BuildingVacantClassroomResponse(BaseModel):
    name: str
    vacantClassroomInfo: List[vacantClassroomInfo]


class SchoolVacantClassroomResponse(BaseModel):
    buildings: List[BuildingVacantClassroomResponse]


class VacantClassroomResponse(BaseModel):
    shahe: SchoolVacantClassroomResponse
    xueyuanlu: SchoolVacantClassroomResponse


@router.get('/getVacantClassroom', tags=['工具箱'], response_model=VacantClassroomResponse)
def get_vacant_classroom(db: Session = Depends(get_db)):
    target = [('shahe', vacant_data['vacant_classroom']['sh']),
              ('xueyuanlu', vacant_data['vacant_classroom']['xyl'])]
    ret = {}
    for name, dic in target:
        res = []
        for k in dic:
            added = {}
            added['name'] = k
            added['vacantClassroomInfo'] = []
            for rec in dic[k]:
                added['vacantClassroomInfo'].append({'name': rec['name'],
                                                     'vacant_time': [int(x) for x in rec['kxsds'].strip().split(',')
                                                                     if x.strip() != '']})
            res.append(added)
        ret[name] = {'buildings': res}
    return ret


class BoyaInfo(BaseModel):
    state: str
    name: str
    type: str
    position: str
    teacher: str
    school: str
    start_time: str
    end_time: str
    select_start_time: str
    select_end_time: str
    unselect_end_time: str
    selected_number: str
    capacity_number: str


@router.get('/getBoyaInfo', tags=['工具箱'], response_model=List[BoyaInfo])
def get_boya_info(db: Session = Depends(get_db)):
    return vacant_data['boya']


class CountRespnse(BaseModel):
    count: int


@router.get('/getComplainAmount', tags=['举报'], response_model=CountRespnse)
def get_complain_amount(db: Session = Depends(get_db), current_user: Optional[dict] = Depends(authorize)):
    if not current_user:
        raise EXC.UniException(key="isSuccess", value=False)
    user = crud.get_user_by_id(db, current_user['uid'])
    if user.privilege == 0:
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "您不是管理员"})
    return {"count": len(crud.get_report_issues(db))}


class ShutUpUserRequest(BaseModel):
    id: int
    day: int
    hour: int
    min: int


@router.post('/shutUpUser', response_model=successResponse, tags=['举报'])
def shut_up_user(req: ShutUpUserRequest, db: Session = Depends(get_db),
                 current_user: Optional[dict] = Depends(authorize)):
    if not current_user:
        raise EXC.UniException(key='isSuccess', value=False)
    user = crud.get_user_by_id(db, current_user['uid'])
    if user.privilege == 0:
        raise EXC.UniException(key='isSuccess', value=False, others={"description": "您不是管理员，无法禁言用户"})
    target_user = crud.shut_up_user(db, req.id, req.day, req.hour, req.min)
    return successResponse()


class IsShutUpResponse(BaseModel):
    isShutUp: bool


class CheckIsShutUpRequest(BaseModel):
    id: int


@router.post('/isShutUpByUserId', response_model=IsShutUpResponse, tags=['举报'])
def shut_up_user(req: CheckIsShutUpRequest, db: Session = Depends(get_db),
                 current_user: Optional[dict] = Depends(authorize)):
    if not current_user:
        raise EXC.UniException(key='isSuccess', value=False)
    target_user = crud.get_user_by_id(db, req.id)
    if not target_user:
        raise EXC.UniException(key='isSuccess', value=False, others={'description': '目标用户id不存在'})
    return IsShutUpResponse(isShutUp=target_user.activate_time > datetime.now())


def check_user_is_shutup(uid: int, db: Session) -> bool:
    return crud.get_user_by_id(db, uid).activate_time > datetime.now()


class ReportIssueItem(BaseModel):
    complainId: int
    blogTitle: str
    blogId: int
    blogContent: str
    commentId: int
    comment: str
    blogAuthorId: int
    commentAuthorId: int
    cause: str
    time: datetime
    isComment: bool
    isAno: bool


@router.get('/getComplainList', response_model=List[ReportIssueItem], tags=['举报'])
def getComplainList(db: Session = Depends(get_db), current_user: Optional[dict] = Depends(authorize)):
    if not current_user:
        raise EXC.UniException(key='isSuccess', value=False)
    user = crud.get_user_by_id(db, current_user['uid'])
    if user.privilege == 0:
        raise EXC.UniException(key='isSuccess', value=False, others={"description": "您不是管理员"})
    issues = crud.get_report_issues(db)
    ret = []
    for issue in issues:
        comment_id = 0
        comment_content = ''
        comment_author_id = 0
        if issue.is_blog:
            blog = issue.blog
            title = blog.title
            blog_content = blog.content
            blog_id = blog.id
            blog_author_id = blog.user_id
            if issue.is_comment:
                comment = issue.blog_comment
                comment_id = comment.id
                comment_content = comment.content
                comment_author_id = comment.user_id
        elif issue.is_question:
            question = crud.get_question_by_id(db, issue.question_id)
            title = question.content
            blog_content = question.content
            blog_id = question.id
            blog_author_id = question.user_id
            if issue.is_comment:
                comment = issue.question_comment
                comment_id = comment.id
                comment_content = comment.content
                comment_author_id = comment.user_id
        else:
            continue

        ret.append(ReportIssueItem(
            complainId=issue.id,
            blogTitle=title,
            blogContent=blog_content,
            blogId=blog_id,
            commentId=comment_id,
            comment=comment_content,
            blogAuthorId=blog_author_id,
            commentAuthorId=comment_author_id,
            cause=issue.reason,
            time=issue.create_at,
            isComment=issue.is_comment,
            isAno=issue.is_blog
        ))
    return ret


class DeleteComplainItemRequest(BaseModel):
    id: int


@router.post('/deleteComplainItem', response_model=successResponse, tags=['举报'])
def delete_complain_item(req: DeleteComplainItemRequest, db: Session = Depends(get_db),
                         current_user: Optional[dict] = Depends(authorize)):
    if not current_user:
        raise EXC.UniException(key='isSuccess', value=False)
    user = crud.get_user_by_id(db, current_user['uid'])
    if user.privilege == 0:
        raise EXC.UniException(key='isSuccess', value=False, others={"description": "您不是管理员"})
    if not crud.get_issue_by_id(db, req.id):
        raise EXC.UniException(key='isSuccess', value=False, others={"description": "该issueid不存在"})
    crud.delete_issue(db, req.id)
    return successResponse()


class ComplainForBlogRequest(BaseModel):
    blogId: int
    cause: str


@router.post('/submitComplainForBlog', tags=['举报'])
def submit_complain_for_blog(req: ComplainForBlogRequest, db: Session = Depends(get_db),
                             current_user: Optional[dict] = Depends(authorize)):
    if not current_user:
        raise EXC.UniException(key='isSuccess', value=False)
    user = crud.get_user_by_id(db, current_user['uid'])
    blog = crud.get_blog_by_blog_id(db, req.blogId)
    if not blog:
        raise EXC.UniException(key='isSuccess', value=False, others={"description": "blog 不存在"})
    crud.report_blog(db, blog.id, user.id, req.cause)
    return {'response': 'success'}


class ComplainForBlogCommentRequest(BaseModel):
    blogId: int
    commentId: int
    cause: str


@router.post('/submitComplainForBlogComment', tags=['举报'])
def submit_complain_for_blog(req: ComplainForBlogCommentRequest, db: Session = Depends(get_db),
                             current_user: Optional[dict] = Depends(authorize)):
    if not current_user:
        raise EXC.UniException(key='isSuccess', value=False)
    user = crud.get_user_by_id(db, current_user['uid'])
    comment = crud.get_blog_comment_by_id(db, req.blogId)
    if not comment:
        raise EXC.UniException(key='isSuccess', value=False, others={"description": "blog comment 不存在"})
    crud.report_blog_comment(db, comment.blog_id, comment.id, user.id, req.cause)
    return {'response': 'success'}
