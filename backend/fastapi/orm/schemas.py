from pydantic import BaseModel

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
    context: str
    is_anonymous: bool

# 用于创建
class BlogCreate(BlogBase):
    user_id: int

class BlogCommentBase(BaseModel):
    blogId: int
    commentContent: str
    ifAnonymous: bool