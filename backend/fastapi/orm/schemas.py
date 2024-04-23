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
    content: str
    ifAnonymous: bool
    imageList: list[str]
    
class BlogCommentBase(BaseModel):
    blogId: int
    commentContent: str
    ifAnonymous: bool