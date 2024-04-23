from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from orm.database import get_db
import orm.schemas as schemas
import orm.crud as crud
from pydantic import BaseModel


router = APIRouter()

@router.get("/blog/getBlogs")
def get_blog_by_page(db: Session = Depends(get_db)):
	pass

class BlogId(BaseModel):
	blogId: int

@router.get("/blog/getBlogByBlogId")
def get_blog_by_blog_id(blog_id: BlogId,
						db: Session = Depends(get_db)):
	blog = crud.get_blog_by_blog_id(db, blog_id.blogId)
	return blog

@router.put("/blog/uploadBlog")
def create_blog(blog: schemas.BlogBase,
				db: Session = Depends(get_db)):
	# blog = schemas.BlogCreate()
	crud.create_blog(db,
					user_id=0,
					title=blog.title,
					context=blog.context,
					is_anonymous=blog.is_anonymous)
	return {"response":"success"}

@router.get("/blog/getCommentsByBlogId")
def get_blog_comment_by_blog_id(db: Session = Depends(get_db)):
	pass

@router.get("/blog/uploadComment")
def create_blog_comment(db: Session = Depends(get_db)):
	pass

