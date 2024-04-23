from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from orm.database import get_db
import orm.schemas as schemas
import orm.crud as crud
from pydantic import BaseModel
from tools.check_user import check_user


router = APIRouter()

class BlogPage(BaseModel):
	pageno: int
	pagesize: int

@router.put("/blog/getBlogs")
def get_blog_by_page(blog_page: BlogPage,
					 db: Session = Depends(get_db)):
	offset = (blog_page.pageno - 1) * blog_page.pagesize
	limit = blog_page.pagesize
	blogs = crud.get_blogs(db, offset=offset, limit=limit, asc=False)
	return blogs

class BlogId(BaseModel):
	blogId: int

@router.put("/blog/getBlogByBlogId")
def get_blog_by_blog_id(blog_id: BlogId,
						db: Session = Depends(get_db)):
	blog = crud.get_blog_by_blog_id(db, blog_id.blogId)
	return blog

@router.put("/blog/uploadBlog")
@check_user
def create_blog(blog: schemas.BlogBase,
				uid: int,
				db: Session = Depends(get_db)):
	db_blog = crud.create_blog(db,
					user_id=uid,
					title=blog.title,
					context=blog.context,
					is_anonymous=blog.is_anonymous)
	if db_blog == None:
		return {"response":"error"}
	else:
		return {"response":"success"}

@router.put("/blog/getCommentsByBlogId")
def get_blog_comment_by_blog_id(db: Session = Depends(get_db)):
	pass

@router.put("/blog/uploadComment")
def create_blog_comment(db: Session = Depends(get_db)):
	pass

