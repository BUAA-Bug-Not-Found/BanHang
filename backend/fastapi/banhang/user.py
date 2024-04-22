import os

from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel

from orm import crud,schemas
from orm.database import get_db

from tools.check_user import generate_jwt_token
from tools.mail import MailSender,is_valid_email
import banhang.BanHangException as EXC
import random

router = APIRouter()

# Dependency



class loginRequest(BaseModel):
    username:str
    password:str
class usernameRequest(BaseModel):
    username:str
class emailRequest(BaseModel):
    email:str
class registerRequest(schemas.UserCreate):
    checkCode:str

@router.put("/login")
def login(req:loginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, req.username)
    if not user or user.password != req.password:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    return{'set-cookie': generate_jwt_token(user.id, user.username), "isSuccess":True}

@router.post("/register")
def register(req:registerRequest, db: Session = Depends(get_db)):
    if not crud.is_valid_checkCode(db, req.checkCode, req.email):
        raise EXC.UniException(key = "isSuccess", value=False, others={"description":"Invalid check"})
    user = crud.get_user_by_username(db, req.username)
    if user:
        raise HTTPException(status_code=400, detail="user exists")
    crud.create_user(db, schemas.UserCreate(username = req.username, password = req.password, email = req.email))
    return {"response":"success"}

@router.get("/banhang/check_username_registered")
def check_username_registered(req:usernameRequest, db:Session = Depends(get_db)):
    user = crud.get_user_by_username(db, req.username)
    if user:
        return {"response":"exists"}
    return {"response":"valid"}

@router.post("/sendCheckCode")
def send_check_code(req: emailRequest, db:Session = Depends(get_db)):
    checkcode = random.choice(range(10000,100000))
    if os.environ.get("CHECKCODE") is not None:
        checkcode = int(os.environ.get("CHECKCODE"))
    if not is_valid_email(req.email):
        raise EXC.UniException(key = "isSuccess", value=False, others={"detail":"invalid email"})
    try:
        if os.environ.get("CHECKCODE") is None:
            MailSender.send(req.email, checkcode)
        crud.create_checkcode_record(db, schemas.EmailCheck(email = req.email, checkcode = checkcode))
        return {"isSuccess":True}
    except:
        raise EXC.UniException(key = "isSuccess", value = False, others={"detail":"内部错误"})