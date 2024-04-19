from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from orm.orm import User
from tools.check_user import generate_jwt_token

router = APIRouter()
class loginRequest(BaseModel):
    username:str
    password:str

@router.put("/banhang/login")
def login(req:loginRequest):
    user = User.select().where(User.username == req.username and User.password == req.password)

    if not len(user):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    user = user[0]
    return{'token': generate_jwt_token(user.uid, user.username)}

@router.put("/banhang/register")
def register(req:loginRequest):
    user = User.select().where(User.username == req.username and User.password == req.password)
    if len(user):
        raise HTTPException(status_code=400, detail="user exists")
    User.create(username = req.username, password = req.password).save()
    return {"response":"success"}