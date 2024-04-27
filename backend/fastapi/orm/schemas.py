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
    tagList: List[int]

class BlogShow(BaseModel):
    userId: int
    userName: str
    userAvatarUrl: Optional[str]
    blogId: int
    title: str
    content: str
    time: datetime
    imageList: List[str]
    tagList: List[str]

class BlogCommentBase(BaseModel):
    blogId: int
    commentContent: str
    ifAnonymous: bool
    replyToCommentId: Optional[int] 
    
class BlogCommentShow(BaseModel):
    userId: int
    userName: str
    userAvatarUrl: Optional[str]
    commentId: int
    commentContent: str
    time: datetime
    replyToCommentId: Optional[int] 

class QuestionCreate(BaseModel):
    content:str
    userId:int
    questionTagids:List[int]
    questionImageids:List[int]

class QuestionImageCreate(BaseModel):
    questionId: int
    imageUrl:str

class QuestionCommentImageCreate(BaseModel):
    questionCommentId: int
    imageUrl:str

class QuestionCommentCreat(BaseModel):
    content:str
    userId:int
    questionCommentImageids: List[int]
    questionId: int = 0