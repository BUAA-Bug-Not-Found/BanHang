from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from orm.database import get_db
import orm.schemas as schemas
import orm.crud as crud
from pydantic import BaseModel, field_validator
from tools.check_user import check_user
from typing import List
from bs4 import BeautifulSoup
from tools.review import review_text
from banhang.user import check_user_is_shutup


def get_blog_from_db_blog(db, db_blog):
    db_images = db_blog.images
    db_user = db_blog.user
    db_tags = db_blog.tags
    blog = {}
    if db_blog.is_anonymous:
        blog['userId'] = -1
        annoy_info = crud.get_user_anony_info_by_blog_id(db, db_blog.id, db_blog.user_id, create=True)
        blog['userName'] = annoy_info.anony_name
        blog['userAvatarUrl'] = annoy_info.anony_avatar_url
    else:
        db_user = db_blog.user
        blog['userId'] = db_user.id
        blog['userName'] = db_user.username
        blog['userAvatarUrl'] = db_user.userAvatarURL
    blog['blogId'] = db_blog.id
    blog['title'] = db_blog.title
    blog['content'] = db_blog.content
    blog['time'] = db_blog.create_at
    blog['commentNum'] = len(db_blog.comments)
    blog['imageList'] = []
    for db_image in db_images:
        blog['imageList'].append(db_image.image_url)
    blog['tagList'] = []
    for db_tag in db_tags:
        tag = {}
        tag['tagId'] = db_tag.id
        tag['tagName'] = db_tag.name
        tag['tagIcon'] = db_tag.icon
        tag['tagColor'] = db_tag.color
        blog['tagList'].append(tag)
    return blog


router = APIRouter()


@router.post("/blog/getBlogs", tags=["Blog"], response_model=List[schemas.BlogShow])
def get_blog_by_page(blog_page: schemas.BlogPageTag,
                     db: Session = Depends(get_db)):
    offset = (blog_page.pageno - 1) * blog_page.pagesize
    limit = blog_page.pagesize
    if blog_page.nowTag == -1:
        db_blogs = crud.get_blogs(db, offset=offset, limit=limit, asc=False, not_deleted=True)
    else:
        db_blogs = crud.get_blogs_by_tag_id(db, blog_page.nowTag, offset, limit, not_deleted=True)
    blogs = []
    for db_blog in db_blogs:
        blog = get_blog_from_db_blog(db, db_blog)
        blogs.append(schemas.BlogShow(**blog))
    return blogs


class BlogId(BaseModel):
    blogId: int


@router.post("/blog/getBlogByBlogId", response_model=schemas.BlogShow, tags=["Blog"])
def get_blog_by_blog_id(blog_id: BlogId,
                        db: Session = Depends(get_db)):
    db_blog = crud.get_blog_by_blog_id(db, blog_id.blogId)
    if db_blog == None:
        return {"response": "error", "description": "No corresponding blog ID exists"}
    if db_blog.status == "deleted":
        return {"response": "error", "description": "Blog has been deleted"}
    blog = get_blog_from_db_blog(db, db_blog)
    return schemas.BlogShow(**blog)


@router.post("/blog/uploadBlog", tags=["Blog"])
@check_user
def create_blog(blog: schemas.BlogBase,
                uid: int,
                db: Session = Depends(get_db)):
    if uid == None:
        return {"response": "error", "description": "Please login first"}
    if check_user_is_shutup(uid, db):
        raise {"response": "error", "description": "用户被禁言"}
    for tag_id in blog.tagList:
        if crud.get_blog_tag_by_id(db, tag_id) == None:
            return {"response": f"No corresponding tag ID ({tag_id}) exists"}
    html = blog.title + blog.content
    soup = BeautifulSoup(html)
    review_result = review_text(soup.get_text())
    if len(review_result.data.label) != 0:
        return {"response":"error",
          "description": review_result.data.label}
    db_blog = crud.create_blog(db,
                               user_id=uid,
                               title=blog.title,
                               content=blog.content,
                               is_anonymous=blog.ifAnonymous,
                               image_urls=blog.imageList,
                               tag_ids=blog.tagList)
    if db_blog == None:
        return {"response": "error"}
    else:
        return {"response": "success"}


@router.post("/blog/deleteBlogByBlogId", tags=["Blog"])
@check_user
def delete_blog_by_blog_id(blog_id: BlogId,
                           uid: int,
                           db: Session = Depends(get_db)):
    if uid == None:
        return {"response": "error", "description": "Please login first"}
    db_blog = crud.get_blog_by_blog_id(db, blog_id.blogId)
    if db_blog == None:
        return {"response": "error", "description": "No corresponding blog ID exists"}
    if db_blog.user_id != uid:
        return {"response": "error", "description": "Permission denied"}
    if db_blog.status == "deleted":
        return {"response": "error", "description": "Blog has been deleted"}
    db_blog.status = "deleted"
    db.add(db_blog)
    db.commit()
    return {"response": "success"}


@router.post("/blog/getCommentsByBlogId", response_model=List[schemas.BlogCommentShow], tags=["Blog"])
def get_blog_comments_by_blog_id(blog_id: BlogId,
                                 db: Session = Depends(get_db)):
    db_blog = crud.get_blog_by_blog_id(db, blog_id.blogId)
    if db_blog == None:
        return {"response": "error", "description": "No corresponding blog ID exists"}
    if db_blog.status == "deleted":
        return {"response": "error", "description": "Blog has been deleted"}
    db_comments = db_blog.comments
    comments = []
    for db_comment in db_comments:
        comment = {}
        if db_comment.is_anonymous:
            comment['userId'] = -1
            annoy_info = crud.get_user_anony_info_by_blog_id(db, db_comment.blog_id, db_comment.user_id, create=True)
            comment['userName'] = annoy_info.anony_name
            comment['userAvatarUrl'] = annoy_info.anony_avatar_url
        else:
            db_user = db_comment.user
            comment['userId'] = db_user.id
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
    if uid == None:
        return {"response": "error", "description": "Please login first"}
    if check_user_is_shutup(uid, db):
        raise {"response": "error", "description": "用户被禁言"}
    db_blog = crud.get_blog_by_blog_id(db, blog_comment.blogId)
    if db_blog == None:
        return {"response": "error", "description": "No corresponding blog ID exists"}
    if db_blog.status == "deleted":
        return {"response": "error", "description": "Blog has been deleted"}
    html = blog_comment.commentContent
    soup = BeautifulSoup(html)
    review_result = review_text(soup.get_text())
    if len(review_result.data.label) != 0:
        return {"response":"error",
          "description": review_result.data.label}
    db_blog_comment = crud.create_blog_comment(db,
                                               user_id=uid,
                                               blog_id=blog_comment.blogId,
                                               content=blog_comment.commentContent,
                                               is_anonymous=blog_comment.ifAnonymous,
                                               reply_to_comment_id=blog_comment.replyToCommentId)
    if db_blog_comment == None:
        return {"response": "error"}
    else:
        host_user_id = 50
        if blog_comment.replyToCommentId == None:

            guest_user_id = db_blog.user_id
            content = f"您的帖子「{db_blog.title}」有了新回复：{blog_comment.commentContent}"
        else:
            guest_user_id = db_blog_comment.reply_to_comment.user_id
            content = f"您在帖子「{db_blog.title}」的评论有了新回复：{blog_comment.commentContent}"
        crud.send_message(db, host_user_id, guest_user_id, content)
        return {"response": "success"}


@router.post("/search/searchBlogAPage", tags=["Blog"], response_model=List[schemas.BlogShow])
def get_blogs_advanced(blog_page_advanced: schemas.BlogPageAdvanced,
                       db: Session = Depends(get_db)):
    offset = (blog_page_advanced.pageno - 1) * blog_page_advanced.pagesize
    limit = blog_page_advanced.pagesize
    if blog_page_advanced.nowSortMethod == "byRelation":
        db_blogs = crud.get_blogs_by_search_content(db, blog_page_advanced.searchContent, offset, limit, asc=False,
                                                    not_deleted=True)
    elif blog_page_advanced.nowSortMethod == "byTime":
        db_blogs = crud.get_blogs_by_search_content(db, blog_page_advanced.searchContent, offset, limit, asc=False,
                                                    not_deleted=True)
    elif blog_page_advanced.nowSortMethod == "byPopularity":
        db_blogs = []
    blogs = []
    for db_blog in db_blogs:
        blog = get_blog_from_db_blog(db, db_blog)
        blogs.append(schemas.BlogShow(**blog))
    return blogs


@router.post("/blog/getAllBlogTags", tags=["Blog"], response_model=List[schemas.TagBase])
def get_all_blog_tags(db: Session = Depends(get_db)):
    db_tags = crud.get_all_blog_tags(db)
    tags = []
    for db_tag in db_tags:
        tag = {}
        tag['tagId'] = db_tag.id
        tag['tagName'] = db_tag.name
        tag['tagIcon'] = db_tag.icon
        tag['tagColor'] = db_tag.color
        tags.append(schemas.TagBase(**tag))
    return tags