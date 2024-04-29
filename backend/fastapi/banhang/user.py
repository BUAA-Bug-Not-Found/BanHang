import os
from datetime import datetime
from typing import Optional, List

from fastapi import Depends, FastAPI, HTTPException, APIRouter, Response, Cookie
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy.sql.functions import user

from banhang import blog
from orm import crud,schemas
from orm.database import get_db

from tools.check_user import generate_jwt_token,authorize
from tools.mail import MailSender,is_valid_email
import banhang.BanHangException as EXC
import random

router = APIRouter()

# Dependency


class successResponse(BaseModel):
    isSuccess:bool = True
class loginRequest(BaseModel):
    email:str
    password:str
class usernameRequest(BaseModel):
    username:str
class emailRequest(BaseModel):
    email:str
class registerRequest(schemas.UserCreate):
    checkCode:str
class resetPasswordRequest(loginRequest):
    checkCode:str
class userResponse(BaseModel):
    username:str
    email:str
    uid:int

class excResponse(BaseModel):
    isSuccess:bool = False
    discription:str

@router.put("/login",tags=["注册登录"], response_model=successResponse,
            responses={400: {"model": excResponse}})
def login(req:loginRequest,response: Response, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, req.email)
    if not user or user.password != req.password:
        raise EXC.UniException(key = "isSuccess", value=False, others={"description":"Invalid username or password"})
    response.set_cookie(key="Auth", value=generate_jwt_token(user.id, user.username), samesite='none',secure=True)
    return {"isSuccess":True}

@router.put("/logout",tags=["注册登录"], response_model=successResponse,
            responses={400: {"model": excResponse}})
def logout(response: Response):
    response.set_cookie(key="Auth", value="logout")
    return{"isSuccess":True}

@router.post("/registerUser",tags=["注册登录"], response_model=successResponse,
             responses={400: {"model": excResponse}})
def register(req:registerRequest, db: Session = Depends(get_db)):
    if not crud.is_valid_checkCode(db, req.checkCode, req.email):
        raise EXC.UniException(key = "isSuccess", value=False, others={"description":"Invalid check"})
    user = crud.get_user_by_email(db, req.email)
    if user:
        raise EXC.UniException(key = "isSuccess", value=False, others={"description":"user exists"})
    crud.create_user(db, schemas.UserCreate(username = req.username, password = req.password, email = req.email))
    return {"isSuccess":True}

@router.get("/check_login_state",tags=["注册登录"], response_model=userResponse,
            responses={400: {"model": excResponse}})
def check_login_state(current_user: Optional[dict] = Depends(authorize),db:Session = Depends(get_db)):
    if current_user:
        current_user["email"] = crud.get_user_by_id(db,current_user["uid"]).email
        return current_user
    raise EXC.UniException(key = "isSuccess", value=False, others={"description":"user not login"})

@router.post("/sendCheckCode",tags=["注册登录"], response_model=successResponse,
             responses={400: {"model": excResponse}})
def send_check_code(req: emailRequest, db:Session = Depends(get_db)):
    checkcode = random.choice(range(10000,100000))
    # print(checkcode)
    if os.environ.get("CHECKCODE") is not None:
        checkcode = int(os.environ.get("CHECKCODE"))
    if not is_valid_email(req.email):
        raise EXC.UniException(key = "isSuccess", value=False, others={"description":"invalid email"})
    try:
        if os.environ.get("CHECKCODE") is None:
            MailSender.send(req.email, checkcode)
            pass
        crud.create_checkcode_record(db, schemas.EmailCheck(email = req.email, checkcode = checkcode))
        return {"isSuccess":True}
    except:
        raise EXC.UniException(key = "isSuccess", value = False, others={"description":"内部错误"})

@router.post("/resetPassword",tags=["注册登录"], response_model=successResponse,
             responses={400: {"model": excResponse}})
def reset_password(req:resetPasswordRequest, db:Session = Depends(get_db)):
    if not crud.is_valid_checkCode(db, req.checkCode, req.email):
        raise EXC.UniException(key = "isSuccess", value=False, others={"description":"Invalid check"})
    user = crud.get_user_by_email(db, req.email)
    if not user:
        raise EXC.UniException(key="isSuccess", value=False, others={"description":"用户不存在"})
    crud.set_password_by_email(db, req.password, req.email)
    return {"response":"success"}

class UserInfoResponse(BaseModel):
    nickname: str
    sign: str
    url: str
    user_id: int
@router.get("/getInfoByEmail", tags=['用户中心'],response_model=UserInfoResponse,
            responses={400: {"model": excResponse}})
def get_info_by_email(email:str, db:Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if not user:
        raise EXC.UniException(key = "isSuccess", value=False, others={"description":"用户不存在"})
    return {"nickname":user.username, "sign":user.sign, 'url':user.userAvatarURL if user.userAvatarURL else "",
            'user_id':user.id}

class SetSignRequest(BaseModel):
    email:str
    sign:str
@router.post("/setSignByEmail", tags=['用户中心'], response_model=successResponse,
             responses={400: {"model": excResponse}})
def set_sign_by_email(req:SetSignRequest,current_user: Optional[dict] = Depends(authorize),
                      db:Session = Depends(get_db)):
    if not current_user:
        raise EXC.UniException(key = "isSuccess", value=False, others={"description":"用户未登录"})
    user = crud.get_user_by_email(db, req.email)
    current_user_instance = crud.get_user_by_id(db, current_user['uid'])
    if current_user_instance.privilege == 0 and current_user_instance.email != user.email:
        raise EXC.UniException(key = "isSuccess", value=False, others={"description":"用户无权限"})
    user = crud.set_sign_by_email(db, req.email, req.sign)
    return successResponse()

class SetNicknameRequest(BaseModel):
    email:str
    nickname:str
@router.post("/setNicknameByEmail", tags=['用户中心'], response_model=successResponse,
             responses={400: {"model": excResponse}})
def set_nickname_by_email(req:SetNicknameRequest,current_user: Optional[dict] = Depends(authorize),
                      db:Session = Depends(get_db)):
    if not current_user:
        raise EXC.UniException(key = "isSuccess", value=False, others={"description":"用户未登录"})
    user = crud.get_user_by_email(db, req.email)
    current_user_instance = crud.get_user_by_id(db, current_user['uid'])
    if current_user_instance.privilege == 0 and current_user_instance.email != user.email:
        raise EXC.UniException(key = "isSuccess", value=False, others={"description":"用户无权限"})
    user = crud.set_username_by_email(db, req.email, req.nickname)
    return successResponse()

class GetAnonyBlogResponse(BaseModel):
    blogTitle:str
    firstPhotoUrl:str
    time: datetime
@router.get("/getAnonyBlogsByEmail", tags=['用户中心'], response_model=List[GetAnonyBlogResponse],
            responses={400: {"model": excResponse}})
def get_anonyBlogs_by_email(email:str,current_user: Optional[dict] = Depends(authorize),
                            db:Session = Depends(get_db)):
    if not current_user:
        raise EXC.UniException(key = "isSuccess", value=False, others={"description":"用户未登录"})
    user = crud.get_user_by_email(db, email)
    current_user_instance = crud.get_user_by_id(db, current_user['uid'])
    if current_user_instance.privilege == 0 and current_user_instance.email != user.email:
        raise EXC.UniException(key = "isSuccess", value=False, others={"description":"用户无权限"})
    blogs = crud.get_blog_by_email(db, email)
    return [GetAnonyBlogResponse(blogTitle = blog.title,
                                 firstPhotoUrl = blog.images[0].image_url if len(blog.images) > 0 else "",
                                 time = blog.create_at)
            for blog in blogs]

@router.get("/getHelpBlogsByEmail", tags=['用户中心'], response_model=List[GetAnonyBlogResponse],
            responses={400: {"model": excResponse}})
def get_helpBlogs_by_email(email:str,current_user: Optional[dict] = Depends(authorize),
                            db:Session = Depends(get_db)):
    if not current_user:
        raise EXC.UniException(key = "isSuccess", value=False, others={"description":"用户未登录"})
    user = crud.get_user_by_email(db, email)
    current_user_instance = crud.get_user_by_id(db, current_user['uid'])
    if current_user_instance.privilege == 0 and current_user_instance.email != user.email:
        raise EXC.UniException(key = "isSuccess", value=False, others={"description":"用户无权限"})
    questions = crud.get_questions_by_email(db, email)
    return [GetAnonyBlogResponse(blogTitle = question.content,
                                 firstPhotoUrl = question.images[0].image_url if len(question.images) > 0 else "",
                                 time = question.create_at)
            for question in questions]

class QueryStarResponse(BaseModel):
    isStar: bool
@router.get("/queryStar", tags=["用户中心"], response_model=QueryStarResponse,
            responses={400: {"model": excResponse}})
def query_star(email1: str, email2: str, db:Session = Depends(get_db)):
    user1 = crud.get_user_by_email(db, email1)
    user2 = crud.get_user_by_email(db, email2)
    if not user1 or not user2:
        raise EXC.UniException(key = "isSuccess", value=False, others={"description":"用户不存在"})
    return {"isStar": user2 in user1.followed}

class SetStarRequest(BaseModel):
    email1: str
    email2: str
    state: bool

@router.post("/setStarState", response_model=successResponse, tags=["用户中心"],
             responses={400: {"model": excResponse}})
def set_star_state(req:SetStarRequest, db:Session = Depends(get_db),
                   current_user: Optional[dict] = Depends(authorize)):
    current_user_isntance = crud.get_user_by_id(db, current_user['uid'])
    user1 = crud.get_user_by_email(db, req.email1)
    user2 = crud.get_user_by_email(db, req.email2)
    if not user1 or not user2:
        raise EXC.UniException(key = "isSuccess", value=False, others={"description":"用户不存在"})
    if current_user_isntance.privilege == 0 and current_user_isntance.email != user1.email:
        raise EXC.UniException(key = "isSuccess", value=False, others={"description":"无权修改别人的follow状态"})
    crud.set_star_state_by_email(db, req.email1, req.email2, is_followed=req.state)
    return successResponse()

class UserResponse(BaseModel):
    nickname:str
    sign:str
    url:str
class UserSearchResponse(BaseModel):
    users: List[UserResponse]
    userSum: int

class SearchQuestionsRequest(BaseModel):
    searchContent:str
    pageno:int
    pagesize:int
    nowSortMethod:str
@router.post("/searchUserAPage", tags=["用户中心"], response_model=UserSearchResponse)
def search_questions_by_content(req:SearchQuestionsRequest,db: Session = Depends(get_db),
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
    db_users= crud.search_user_by_word(db, req.searchContent, offset=offset, limit=limit)
    users = [{'nickname':user.username, 'sign':user.sign, 'url':user.userAvatarURL if user.userAvatarURL else ""}
             for user in db_users]
    return {"users": users,
            "userSum": crud.get_search_user_sum_by_word(db, req.searchContent, offset=offset, limit=limit)}

class FansResponse(BaseModel):
    email: str
    headUrl: str
    nickname: str
class getFansResponse(BaseModel):
    fans: List[FansResponse]

@router.get("/getFansByEmail", tags=['用户中心'], response_model=getFansResponse)
def get_fans_by_email(email:str,db: Session = Depends(get_db),
                      current_user: Optional[dict] = Depends(authorize)):
    user = crud.get_user_by_email(db, email)
    if user is None:
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "用户不存在"})
    fans = [{'email':fan.email, 'headUrl':fan.userAvatarURL, 'nickname':fan.username}
            for fan in user.followers]
    return {'fans':fans}

class getStarsResponse(BaseModel):
    stars: List[FansResponse]

@router.get("/getStarsByEmail", tags=['用户中心'], response_model=getStarsResponse)
def get_stars_by_email(email:str, db: Session = Depends(get_db),
                      current_user: Optional[dict] = Depends(authorize)):
    user = crud.get_user_by_email(db, email)
    if user is None:
        raise EXC.UniException(key="isSuccess", value=False, others={"description": "用户不存在"})
    fans = [{'email':fan.email, 'headUrl':fan.userAvatarURL, 'nickname':fan.username}
            for fan in user.followed]
    return {'stars':fans}