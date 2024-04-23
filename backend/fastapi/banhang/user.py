import os
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, APIRouter, Response, Cookie
from sqlalchemy.orm import Session
from pydantic import BaseModel

from orm import crud,schemas
from orm.database import get_db

from tools.check_user import generate_jwt_token,authorize
from tools.mail import MailSender,is_valid_email
import banhang.BanHangException as EXC
import random

router = APIRouter()

# Dependency


class successResponse(BaseModel):
    isSuccess:bool
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
class idAndUsernameResponse(BaseModel):
    username:str
    id:int

class excResponse(BaseModel):
    isSuccess:bool = False
    discription:str

@router.put("/login",tags=["注册登录"], response_model=successResponse,
            responses={400: {"model": excResponse}})
def login(req:loginRequest,response: Response, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, req.email)
    if not user or user.password != req.password:
        raise EXC.UniException(key = "isSuccess", value=False, others={"description":"Invalid username or password"})
    response.set_cookie(key="Auth", value=generate_jwt_token(user.id, user.username))
    return{"isSuccess":True}

@router.post("/registerUser",tags=["注册登录"], response_model=successResponse,
             responses={400: {"model": excResponse}})
def register(req:registerRequest, db: Session = Depends(get_db)):
    if not crud.is_valid_checkCode(db, req.checkCode, req.email):
        raise EXC.UniException(key = "isSuccess", value=False, others={"description":"Invalid check"})
    user = crud.get_user_by_username(db, req.username)
    if user:
        raise EXC.UniException(key = "isSuccess", value=False, others={"description":"user exists"})
    crud.create_user(db, schemas.UserCreate(username = req.username, password = req.password, email = req.email))
    return {"isSuccess":True}

@router.get("/check_login_state",tags=["注册登录"], response_model=idAndUsernameResponse,
            responses={400: {"model": excResponse}})
def check_login_state(current_user: Optional[dict] = Depends(authorize)):
    if current_user:
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
