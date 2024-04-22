from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from orm.database import get_db


router = APIRouter()

@router.get("/blog/getBlogs")
def get_blog_by_page(db: Session = Depends(get_db)):
	pass

@router.get("/blog/getBlogByBlogId")
def get_blog_by_blog_id(db: Session = Depends(get_db)):
	pass

@router.put("/blog/uploadBlog")
def create_blog(db: Session = Depends(get_db)):
	pass

@router.get("/blog/getCommentsByBlogId")
def get_blog_comment_by_blog_id(db: Session = Depends(get_db)):
	pass

@router.get("/blog/uploadComment")
def create_blog_comment(db: Session = Depends(get_db)):
	pass

