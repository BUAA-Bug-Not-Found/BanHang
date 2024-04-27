import datetime

from sqlalchemy.orm import Session
from orm import models, schemas
from sqlalchemy import or_, and_
from orm.models import Message, Conversation


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, password=user.password, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_checkcode_record(db: Session, record: schemas.EmailCheck):
    if tmp := db.query(models.CheckCode).filter(models.CheckCode.email == record.email).first():
        db.delete(tmp)
    db_check_rec = models.CheckCode(email=record.email, checkcode=record.checkcode)
    db.add(db_check_rec)
    db.commit()
    db.refresh(db_check_rec)
    return db_check_rec


def is_valid_checkCode(db: Session, checkcode: str, email: str):
    if not checkcode.isdigit():
        return False
    checkcode = int(checkcode)
    if checkcode_rec := db.query(models.CheckCode).filter(models.CheckCode.email == email).first():
        return (datetime.datetime.now() < checkcode_rec.create_at + datetime.timedelta(minutes=10) and
                checkcode_rec.checkcode == checkcode)
    return False


def set_password_by_email(db: Session, password: str, email: str):
    user = get_user_by_email(db, email)
    user.password = password
    db.commit()


def create_blog(db: Session, user_id: int, title: str, content: str, is_anonymous: bool, image_urls: list[str], tag_ids: list[int]):
    db_blog = models.Blog(user_id=user_id,
                          title=title,
                          content=content,
                          is_anonymous=is_anonymous)
    try:
        db.add(db_blog)
        db.commit()
        db.refresh(db_blog)
        for image_url in image_urls:
            db_image = models.BlogImage(blog_id=db_blog.id, image_url=image_url)
            db.add(db_image)
        for tag_id in tag_ids:
            db_blog_tag = models.BlogBlogTag(blog_id=db_blog.id, tag_id=tag_id)
            db.add(db_blog_tag)
    except Exception as e:
        db.rollback()
        db_blog = None
    return db_blog


def get_blog_by_blog_id(db: Session, blog_id: int):
    return db.query(models.Blog).filter(models.Blog.id == blog_id).first()


def get_blogs(db: Session, offset: int = 0, limit: int = 10, asc: bool = False):
    if asc:
        return db.query(models.Blog).order_by(models.Blog.create_at.asc()).offset(offset).limit(limit).all()
    else:
        return db.query(models.Blog).order_by(models.Blog.create_at.desc()).offset(offset).limit(limit).all()


def get_blog_images_by_blog_id(db: Session, blog_id: int):
    return db.query(models.BlogImage).filter(models.BlogImage.id == blog_id).all()


def get_blog_comments_by_blog_id(db: Session, blog_id: int):
    return db.query(models.BlogComment).filter(models.BlogComment.blog_id == blog_id).all()


def create_blog_comment(db: Session, user_id: int, blog_id: int, content: str, is_anonymous: bool, reply_to_comment_id: int = None):
    db_blog_comment = models.BlogComment(user_id=user_id, blog_id=blog_id, content=content, is_anonymous=is_anonymous, reply_to_comment_id=reply_to_comment_id)
    try:
        db.add(db_blog_comment)
        db.commit()
        db.refresh(db_blog_comment)
    except Exception as e:
        db.rollback()
        db_blog_comment = None
        # print("Error during commit: ", e)
    return db_blog_comment


def get_questions(db: Session, offset: int = 0, limit: int = 10, asc: bool = False):
    if asc:
        return db.query(models.Question).order_by(models.Question.create_at.asc()).offset(offset).limit(limit).all()
    else:
        return db.query(models.Question).order_by(models.Question.create_at.desc()).offset(offset).limit(limit).all()

def get_question_num(db:Session ):
    return len(db.query(models.Question).all())

def get_all_question_tags(db: Session):
    return db.query(models.QuestionTag.id).all()


def get_question_tag_by_name(db: Session, name: str):
    name = name.strip()
    return db.query(models.QuestionTag).filter(models.QuestionTag.name == name).first()


def create_question_tag(db: Session, name: str):
    name = name.strip()
    if tag := get_question_tag_by_name(db, name):
        return tag
    tag = models.QuestionTag(name=name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag

def get_question_tag_by_id(db: Session, id: int):
    return db.query(models.QuestionTag).filter(models.QuestionTag.id == id).first()

def get_question_image_by_id(db: Session, id: int):
    return db.query(models.QuestionImage).filter(models.QuestionImage.id == id).first()

def create_question(db: Session, questionCreat: schemas.QuestionCreate):
    question = models.Question(user_id = questionCreat.userId, content = questionCreat.content,
                               images = [get_question_image_by_id(db, imageid)
                                         for imageid in questionCreat.questionImageids],
                               tags = [get_question_tag_by_id(db, tagid)
                                       for tagid in questionCreat.questionTagids])
    db.add(question)
    db.commit()
    db.refresh(question)
    return question

def get_question_by_id(db: Session, id: int)->models.Question:
    return db.query(models.Question).filter(models.Question.id == id).first()

def update_question(db: Session,qid:int,  questionCreat: schemas.QuestionCreate):
    question = get_question_by_id(db, qid)
    question.content = questionCreat.content
    question.images = [get_question_image_by_id(db, imageid)
                                         for imageid in questionCreat.questionImageids]
    question.tags = [get_question_tag_by_id(db, tagid)
                                       for tagid in questionCreat.questionTagids]
    db.commit()
    db.refresh(question)
    return question

def get_conversation(db: Session, host_user_id: int, guest_user_id: int):
    return db.query(Conversation).filter(and_(Conversation.host_user_id == host_user_id, Conversation.guest_user_id == guest_user_id)).first()

def create_conversation(db: Session, host_user_id: int, guest_user_id: int):
    db_conversation = Conversation(host_user_id=host_user_id, guest_user_id=guest_user_id)
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

def get_recent_conversation(db: Session, user_id: int):
    return db.query(Conversation).filter(Conversation.host_user_id == user_id).order_by(Conversation.update_at.desc()).all()

def create_message(db: Session, sender_id: int, receiver_id: int, content: str):
    db_message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message