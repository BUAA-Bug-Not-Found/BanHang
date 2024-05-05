from pydantic import BaseModel, field_validator
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

class TagBase(BaseModel):
    tagId: int
    tagName: str
    tagIcon: str
    tagColor: str

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
    tagList: List[TagBase]
    commentNum: int

class BlogPage(BaseModel):
	pageno: int
	pagesize: int
	
	@field_validator('pageno')
	@classmethod
	def validate_pageno(cls, value: int) -> int:
		if value <= 0:
			raise ValueError("Illegal blog pageno. Must be greater than 0.")
		return value
	
	@field_validator('pagesize')
	@classmethod
	def validate_pagesize(cls, value: int):
		if value <= 0:
			raise ValueError("Illegal blog pagesize. Must be greater than 0.")
		return value

class BlogPageTag(BlogPage):
	nowTag: int
    
class BlogPageAdvanced(BlogPage):
    searchContent: str
    nowSortMethod: str

    @field_validator('nowSortMethod')
    @classmethod
    def validate_nowSortMethod(cls, value: str) -> str:
        if value not in ['byRelation', 'byTime', 'byPopularity']:
            raise ValueError("Illegal blog sort method. Must be 'byRelation', 'byTime' or 'byPopularity'.")
        return value

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
class MessageShow(BaseModel):
    senderName: str
    senderId: int
    receiverName: str
    receiverId: int
    content: str
    time: datetime
    read: bool
