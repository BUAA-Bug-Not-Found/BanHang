from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    email: str
    username: str

class EmailCheck(BaseModel):
    email:str
    checkcode:int

class BlogBase(BaseModel):
    title: str
    content: str
    ifAnonymous: bool
    imageList: List[str]

class BlogShow(BaseModel):
    userId: int
    userName: str
    userAvatarUrl: str
    blogId: int
    title: str
    content: str
    time: datetime
    imageList: Optional[List[str]]

class BlogCommentBase(BaseModel):
    blogId: int
    commentContent: str
    ifAnonymous: bool
    
class BlogCommentShow(BaseModel):
    userId: int
    userName: str
    userAvatarUrl: str
    commentId: int
    commentContent: str
    time: datetime