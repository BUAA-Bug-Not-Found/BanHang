from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from orm.database import get_db
import orm.schemas as schemas
import orm.crud as crud
from pydantic import BaseModel
from tools.check_user import check_user
from typing import List


router = APIRouter()

class BlogPage(BaseModel):
	pageno: int
	pagesize: int

@router.put("/blog/getBlogs", tags=["Blog"])
def get_blog_by_page(blog_page: BlogPage,
					 db: Session = Depends(get_db)):
	offset = (blog_page.pageno - 1) * blog_page.pagesize
	limit = blog_page.pagesize
	db_blogs = crud.get_blogs(db, offset=offset, limit=limit, asc=False)
	blogs = []
	for db_blog in db_blogs:
		db_images = db_blog.images
		db_user = crud.get_user_by_id(db, db_blog.user_id)
		blog = {}
		blog['userId'] = db_user.id
		blog['username'] = db_user.username
		# blog['userAvatarUrl'] = 
		blog['blogId'] = db_blog.id
		blog['title'] = db_blog.title
		blog['content'] = db_blog.content
		blog['time'] = db_blog.create_at
		blog['imageList'] = []
		for db_image in db_images:
			blog['imageList'].append(db_image.image_url)
		blogs.append(schemas.BlogShow(**blog))
	return blogs

class BlogId(BaseModel):
	blogId: int

@router.put("/blog/getBlogByBlogId", tags=["Blog"], response_model=schemas.BlogShow)
def get_blog_by_blog_id(blog_id: BlogId,
						db: Session = Depends(get_db)):
	db_blog = crud.get_blog_by_blog_id(db, blog_id.blogId)
	db_images = db_blog.images
	db_user = crud.get_user_by_id(db, db_blog.user_id)
	blog = {}
	blog['userId'] = db_user.id
	blog['username'] = db_user.username
	# blog['userAvatarUrl'] = 
	blog['blogId'] = db_blog.id
	blog['title'] = db_blog.title
	blog['content'] = db_blog.content
	blog['time'] = db_blog.create_at
	blog['imageList'] = []
	for db_image in db_images:
		blog['imageList'].append(db_image.image_url)
	return schemas.BlogShow(**blog)

@router.put("/blog/uploadBlog", response_model=List[schemas.Blog], tags=["Blog"])
@check_user
def create_blog(blog: schemas.BlogBase,
				uid: int,
				db: Session = Depends(get_db)):
	db_blog = crud.create_blog(db,
					user_id=uid,
					title=blog.title,
					content=blog.content,
					is_anonymous=blog.ifAnonymous,
					image_urls=blog.imageList)
	if db_blog == None:
		return {"response":"error"}
	else:
		return {"response":"success"}

@router.put("/blog/getCommentsByBlogId", response_model=List[schemas.BlogCommentShow], tags=["Blog"])
def get_blog_comments_by_blog_id(blog_id: BlogId,
								 db: Session = Depends(get_db)):
	db_comments = crud.get_blog_comments_by_blog_id(db, blog_id.blogId)
	comments = []
	for db_comment in db_comments:
		db_user = crud.get_user_by_id(db, db_comment.user_id)
		comment = {}
		comment['userId'] = db_user.user_id
		comment['userName'] = db_user.username
		# comment['userAvatarUrl'] = 
		comment['commentId'] = db_comment.id
		comment['commentContent'] = db_comment.content
		comment['time'] = db_comment.create_at
		comments.append(schemas.BlogCommentShow(**comment))
	return comments

@router.put("/blog/uploadComment", tags=["Blog"])
@check_user
def create_blog_comment(blog_comment: schemas.BlogCommentBase,
						uid: int,
						db: Session = Depends(get_db)):
	db_blog_comment = crud.create_blog_comment(db,
					user_id=uid,
					blog_id=blog_comment.blogId,
					content=blog_comment.commentContent,
					is_anonymous=blog_comment.ifAnonymous)
	if db_blog_comment == None:
		return {"response":"error"}
	else:
		return {"response":"success"}