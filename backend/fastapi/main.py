from typing import Union

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from orm.orm import User
from tools.check_user import generate_jwt_token

app = FastAPI()


class loginRequest(BaseModel):
    username:str
    password:int

@app.put("/banhang/login")
def login(req:loginRequest):
    user = User.select().where(User.username == req.username and User.password == req.password)

    if not len(user):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    user = user[0]
    return{'token': generate_jwt_token(user.uid, user.username)}

@app.put("/banhang/register")
def register(req:loginRequest):
    user = User.select().where(User.username == req.username and User.password == req.password)
    if len(user):
        return HTTPException(status_code=400, detail="user exists")
    User.create(username = req.username, password = req.password).save()
    return {"response":"success"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)