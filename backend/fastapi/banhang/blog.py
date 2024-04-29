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
	nowTag: int

@router.post("/blog/getBlogs", tags=["Blog"], response_model=List[schemas.BlogShow])
def get_blog_by_page(blog_page: BlogPage,
					 db: Session = Depends(get_db)):
	offset = (blog_page.pageno - 1) * blog_page.pagesize
	limit = blog_page.pagesize
	if blog_page.nowTag == -1:
		db_blogs = crud.get_blogs(db, offset=offset, limit=limit, asc=False)
	else:
		db_blogs = crud.get_blogs_by_tag_id(db, blog_page.nowTag, offset, limit)
	blogs = []
	for db_blog in db_blogs:
		db_images = db_blog.images
		db_user = db_blog.user
		db_tags = db_blog.tags
		blog = {}
		blog['userId'] = db_user.id
		blog['userName'] = db_user.username
		blog['userAvatarUrl'] = db_user.userAvatarURL
		blog['blogId'] = db_blog.id
		blog['title'] = db_blog.title
		blog['content'] = db_blog.content
		blog['time'] = db_blog.create_at
		blog['imageList'] = []
		for db_image in db_images:
			blog['imageList'].append(db_image.image_url)
		blog['tagList'] = []
		for db_tag in db_tags:
			blog['tagList'].append(db_tag.names)
		blogs.append(schemas.BlogShow(**blog))
	return blogs

class BlogId(BaseModel):
	blogId: int

@router.post("/blog/getBlogByBlogId", response_model=schemas.BlogShow, tags=["Blog"])
def get_blog_by_blog_id(blog_id: BlogId,
						db: Session = Depends(get_db)):
	db_blog = crud.get_blog_by_blog_id(db, blog_id.blogId)
	db_images = db_blog.images
	db_user = db_blog.user
	db_tags = db_blog.tags
	blog = {}
	blog['userId'] = db_user.id
	blog['userName'] = db_user.username
	blog['userAvatarUrl'] = db_user.userAvatarURL
	blog['blogId'] = db_blog.id
	blog['title'] = db_blog.title
	blog['content'] = db_blog.content
	blog['time'] = db_blog.create_at
	blog['imageList'] = []
	for db_image in db_images:
		blog['imageList'].append(db_image.image_url)
	blog['tagList'] = []
	for db_tag in db_tags:
		blog['tagList'].append(db_tag.names)
	return schemas.BlogShow(**blog)

@router.post("/blog/uploadBlog", tags=["Blog"])
@check_user
def create_blog(blog: schemas.BlogBase,
				uid: int,
				db: Session = Depends(get_db)):
	db_blog = crud.create_blog(db,
					user_id=uid,
					title=blog.title,
					content=blog.content,
					is_anonymous=blog.ifAnonymous,
					image_urls=blog.imageList,
					tag_ids=blog.tagList)
	if db_blog == None:
		return {"response":"error"}
	else:
		return {"response":"success"}

@router.post("/blog/getCommentsByBlogId", response_model=List[schemas.BlogCommentShow], tags=["Blog"])
def get_blog_comments_by_blog_id(blog_id: BlogId,
								 db: Session = Depends(get_db)):
	db_comments = crud.get_blog_comments_by_blog_id(db, blog_id.blogId)
	comments = []
	for db_comment in db_comments:
		db_user = crud.get_user_by_id(db, db_comment.user_id)
		comment = {}
		comment['userId'] = db_user.user_id
		comment['userName'] = db_user.username
		comment['userAvatarUrl'] = db_user.userAvatarURL
		comment['commentId'] = db_comment.id
		comment['commentContent'] = db_comment.content
		comment['time'] = db_comment.create_at
		comment['replyToCommentId'] = db_comment.reply_to_comment_id
		comments.append(schemas.BlogCommentShow(**comment))
	return comments

@router.post("/blog/uploadComment", tags=["Blog"])
@check_user
def create_blog_comment(blog_comment: schemas.BlogCommentBase,
						uid: int,
						db: Session = Depends(get_db)):
	db_blog_comment = crud.create_blog_comment(db,
					user_id=uid,
					blog_id=blog_comment.blogId,
					content=blog_comment.commentContent,
					is_anonymous=blog_comment.ifAnonymous,
					reply_to_comment_id=blog_comment.replyToCommentId)
	if db_blog_comment == None:
		return {"response":"error"}
	else:
		return {"response":"success"}
	
class BlogPageAdvanced(BaseModel):
	searchContent: str
	nowSortMethod: str
	pageno: int
	pagesize: int
	
	
@router.post("/search/searchBlogAPage", tags=["Blog"], response_model=List[schemas.BlogShow])
def get_blogs_advanced(blog_page_advanced: BlogPage,
					 db: Session = Depends(get_db)):
	offset = (blog_page_advanced.pageno - 1) * blog_page_advanced.pagesize
	limit = blog_page_advanced.pagesize
	if  blog_page_advanced.nowSortMethod == "byRelation":
		db_blogs = crud.get_blogs_by_search_content(db, blog_page_advanced.searchContent, offset, limit, asc=False)
	elif blog_page_advanced.nowSortMethod == "byTime":
		db_blogs = crud.get_blogs(db, offset=offset, limit=limit, asc=False)
	elif blog_page_advanced.nowSortMethod == "byPopularity":
		db_blogs = []
	blogs = []
	for db_blog in db_blogs:
		db_images = db_blog.images
		db_user = db_blog.user
		db_tags = db_blog.tags
		blog = {}
		blog['userId'] = db_user.id
		blog['userName'] = db_user.username
		blog['userAvatarUrl'] = db_user.userAvatarURL
		blog['blogId'] = db_blog.id
		blog['title'] = db_blog.title
		blog['content'] = db_blog.content
		blog['time'] = db_blog.create_at
		blog['imageList'] = []
		for db_image in db_images:
			blog['imageList'].append(db_image.image_url)
		blog['tagList'] = []
		for db_tag in db_tags:
			blog['tagList'].append(db_tag.names)
		blogs.append(schemas.BlogShow(**blog))
	return blogs