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

@router.put("/login")
def login(req:loginRequest,response: Response, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, req.email)
    if not user or user.password != req.password:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    response.set_cookie(key="Auth", value=generate_jwt_token(user.id, user.username))
    return{"isSuccess":True}

@router.post("/registerUser")
def register(req:registerRequest, db: Session = Depends(get_db)):
    if not crud.is_valid_checkCode(db, req.checkCode, req.email):
        raise EXC.UniException(key = "isSuccess", value=False, others={"description":"Invalid check"})
    user = crud.get_user_by_username(db, req.username)
    if user:
        raise HTTPException(status_code=400, detail="user exists")
    crud.create_user(db, schemas.UserCreate(username = req.username, password = req.password, email = req.email))
    return {"response":"success"}

@router.get("/check_login_state")
def check_username_registered(current_user: Optional[dict] = Depends(authorize)):
    if current_user:
        return current_user
    return {"response":"invalid"}

@router.post("/sendCheckCode")
def send_check_code(req: emailRequest, db:Session = Depends(get_db)):
    checkcode = random.choice(range(10000,100000))
    # print(checkcode)
    if os.environ.get("CHECKCODE") is not None:
        checkcode = int(os.environ.get("CHECKCODE"))
    if not is_valid_email(req.email):
        raise EXC.UniException(key = "isSuccess", value=False, others={"detail":"invalid email"})
    try:
        if os.environ.get("CHECKCODE") is None:
            MailSender.send(req.email, checkcode)
            pass
        crud.create_checkcode_record(db, schemas.EmailCheck(email = req.email, checkcode = checkcode))
        return {"isSuccess":True}
    except:
        raise EXC.UniException(key = "isSuccess", value = False, others={"detail":"内部错误"})

@router.post("/resetPassword")
def reset_password(req:resetPasswordRequest, db:Session = Depends(get_db)):
    if not crud.is_valid_checkCode(db, req.checkCode, req.email):
        raise EXC.UniException(key = "isSuccess", value=False, others={"description":"Invalid check"})
    user = crud.get_user_by_email(db, req.email)
    if not user:
        raise HTTPException(status_code=400, detail="user exists")
    crud.set_password_by_email(db, req.password, req.email)
    return {"response":"success"}
