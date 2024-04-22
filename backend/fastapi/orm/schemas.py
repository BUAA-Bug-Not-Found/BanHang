from pydantic import BaseModel

class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    email: str = None

class EmailCheck(BaseModel):
    email:str
    checkcode:int
