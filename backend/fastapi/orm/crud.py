import datetime

from sqlalchemy.orm import Session
from orm import models,schemas

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username,password = user.password, email = user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_checkcode_record(db: Session, record: schemas.EmailCheck):
    if tmp := db.query(models.CheckCode).filter(models.CheckCode.email == record.email).first():
        db.delete(tmp)
    db_check_rec = models.CheckCode(email = record.email, checkcode = record.checkcode)
    db.add(db_check_rec)
    db.commit()
    db.refresh(db_check_rec)
    return db_check_rec

def is_valid_checkCode(db: Session, checkcode: str, email:str):
    if not checkcode.isdigit():
        return False
    checkcode = int(checkcode)
    if checkcode_rec := db.query(models.CheckCode).filter(models.CheckCode.email == email).first():
        return (datetime.datetime.now()<checkcode_rec.create_at+datetime.timedelta(minutes=10) and
                checkcode_rec.checkcode == checkcode)
    return False

def set_password_by_email(db: Session, password:str, email:str):
    user = get_user_by_email(db, email)
    user.password = password
    db.commit()

def create_blog(db: Session, user_id: int, title: str, content: str, is_anonymous: bool):
    db_blog = models.Blog(user_id=user_id,
                          title=title,
                          content=content,
                          is_anonymous=is_anonymous)
    try:
        db.add(db_blog)
        db.commit()
        db.refresh(db_blog)
    except Exception as e:
        db.rollback()
        db_blog = None
        # print("Error during commit: ", e)
    return db_blog

def get_blog_by_blog_id(db: Session, blog_id: int):
    return db.query(models.Blog).filter(models.Blog.id == blog_id).first()

def get_blogs(db: Session, offset: int = 0, limit: int = 10, asc: bool = False):
    if asc:
        return db.query(models.Blog).order_by(models.Blog.create_at.asc()).offset(offset).limit(limit).all()
    else:
        return db.query(models.Blog).order_by(models.Blog.create_at.desc()).offset(offset).limit(limit).all()

def get_blog_comments_by_blog_id(db: Session, blog_id: int):
    return db.query(models.BlogComment).filter(models.BlogComment.blog_id == blog_id).all()

def create_blog_comment(db: Session, user_id: int, blog_id: int, content: str, is_anonymous: bool):
    db_blog_comment = models.BlogComment(user_id=user_id, blog_id=blog_id, content=content, is_anonymous=is_anonymous)
    try:
        db.add(db_blog_comment)
        db.commit()
        db.refresh(db_blog_comment)
    except Exception as e:
        db.rollback()
        db_blog_comment = None
        # print("Error during commit: ", e)
    return db_blog_comment