from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel

from orm import crud,schemas
from orm.database import get_db

from tools.check_user import generate_jwt_token


router = APIRouter()

# Dependency



class loginRequest(BaseModel):
    username:str
    password:str

@router.put("/banhang/login")
def login(req:loginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, req.username)
    if not user or user.password != req.password:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    return{'token': generate_jwt_token(user.id, user.username)}

@router.put("/banhang/register")
def register(req:schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, req.username)
    if user:
        raise HTTPException(status_code=400, detail="user exists")
    crud.create_user(db, req)
    return {"response":"success"}
