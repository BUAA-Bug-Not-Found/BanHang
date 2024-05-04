import datetime
from typing import List, Type

from sqlalchemy.orm import Session
from orm import models, schemas
from sqlalchemy import or_, and_, desc
from orm.models import Message, Conversation, ConversationMessage, User


def get_user_by_id(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def search_user_by_word(db: Session, word: str, offset: int, limit: int)-> list[Type[User]]:
    return (db.query(models.User)
            .filter(or_(*[models.User.username.like(f"%{word}%")],
                        *[models.User.email.like(f"%{word}%")]))
            .order_by(models.User.create_at.asc())
            .offset(offset).limit(limit).all())

def get_search_user_sum_by_word(db: Session, word: str, offset: int, limit: int):
    return len((db.query(models.User)
            .filter(or_(*[models.User.username.like(f"%{word}%")],
                        *[models.User.email.like(f"%{word}%")]))
            .order_by(models.User.create_at.asc()).all()))

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, password=user.password, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def set_user_head_url_by_email(db: Session, email:str, url):
    user = get_user_by_email(db, email)
    user.userAvatarURL = url
    db.commit()
    db.refresh(user)
    return user


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


def set_sign_by_email(db: Session, email: str, sign: str):
    user = get_user_by_email(db, email)
    user.sign = sign
    db.commit()
    db.refresh(user)
    return user


def set_username_by_email(db: Session, email: str, username: str):
    user = get_user_by_email(db, email)
    user.username = username
    db.commit()
    db.refresh(user)
    return user


def set_star_state_by_email(db: Session, email1: str, email2: str, is_followed: bool):
    user1 = get_user_by_email(db, email1)
    user2 = get_user_by_email(db, email2)
    if is_followed:
        if user2 not in user1.followed:
            user1.followed.append(user2)
            db.commit()
    else:
        if user2 in user1.followed:
            user1.followed.remove(user2)
            db.commit()


def create_blog(db: Session, user_id: int, title: str, content: str, is_anonymous: bool, image_urls: list[str],
                tag_ids: list[int]):
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
            db_blog_tag = models.BlogBlogTag(blog_id=db_blog.id, blog_tag_id=tag_id)
            db.add(db_blog_tag)
        db.commit()
        db.refresh(db_blog)
    except Exception as e:
        db.rollback()
        db_blog = None
    return db_blog


def get_blog_by_blog_id(db: Session, blog_id: int):
    return db.query(models.Blog).filter(models.Blog.id == blog_id).first()


def get_blog_by_email(db: Session, email: str):
    user = get_user_by_email(db, email)
    return db.query(models.Blog).filter(models.Blog.user_id == user.id).all()


def get_blogs(db: Session, offset: int = 0, limit: int = 10, asc: bool = False):
    return (db.query(models.Blog)
            .order_by(models.Blog.create_at.asc() if asc else models.Blog.create_at.desc())
            .offset(offset).limit(limit).all())

def get_blogs_by_tag_id(db: Session, blog_tag_id: int, offset: int = 0, limit: int = 10, asc: bool = False):
    return (db.query(models.Blog).join(models.BlogTag, models.Blog.tags)
            .filter(models.BlogTag.id == blog_tag_id)
            .order_by(models.Blog.create_at.asc() if asc else models.Blog.create_at.desc())
            .offset(offset).limit(limit).all())

def get_blogs_by_search_content(db: Session, search_content: str, offset: int, limit: int, asc: int):
    word_list = [x.strip() for x in search_content.split(" ") if x != ""]
    return (db.query(models.Blog)
            .filter(or_(*[models.Blog.content.like(f"%{word}%") for word in word_list]))
            .order_by(models.Blog.create_at.asc() if asc else models.Blog.create_at.desc())
            .offset(offset).limit(limit).all())

def get_blog_images_by_blog_id(db: Session, blog_id: int):
    return db.query(models.BlogImage).filter(models.BlogImage.id == blog_id).all()


def get_blog_comments_by_blog_id(db: Session, blog_id: int):
    return db.query(models.BlogComment).filter(models.BlogComment.blog_id == blog_id).all()


def create_blog_comment(db: Session, user_id: int, blog_id: int, content: str, is_anonymous: bool,
                        reply_to_comment_id: int = None):
    db_blog_comment = models.BlogComment(user_id=user_id, blog_id=blog_id, content=content, is_anonymous=is_anonymous,
                                         reply_to_comment_id=reply_to_comment_id)
    try:
        db.add(db_blog_comment)
        db.commit()
        db.refresh(db_blog_comment)
    except Exception as e:
        db.rollback()
        db_blog_comment = None
        # print("Error during commit: ", e)
    return db_blog_comment


def get_all_blog_tags(db: Session):
    return (db.query(models.BlogTag).all())


def get_questions(db: Session, offset: int = 0, limit: int = 10, asc: bool = False):
    if asc:
        return db.query(models.Question).order_by(models.Question.create_at.asc()).offset(offset).limit(limit).all()
    else:
        return db.query(models.Question).order_by(models.Question.create_at.desc()).offset(offset).limit(limit).all()

def get_questions_by_tag_id(db: Session, offset: int = 0, limit: int = 10, asc: bool = False, tag_id: int = 1):
    tag = get_question_tag_by_id(db, tag_id)
    questions = [q for q in tag.questions]
    if asc:
        return sorted(questions, key=lambda q: q.create_at)[offset:offset+limit]
    else:
        return sorted(questions, key=lambda q: q.create_at)[offset:offset+limit]

def get_question_sum_by_tag_id(db: Session, tag_id):
    return len(get_question_tag_by_id(db, tag_id).questions)

def get_question_num(db: Session):
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


def get_question_tag_by_id(db: Session, id: int)->models.QuestionTag:
    return db.query(models.QuestionTag).filter(models.QuestionTag.id == id).first()


def get_question_tag_all(db: Session):
    return db.query(models.QuestionTag).all()


def get_question_image_by_id(db: Session, id: int):
    return db.query(models.QuestionImage).filter(models.QuestionImage.id == id).first()


def create_question(db: Session, questionCreat: schemas.QuestionCreate) -> models.Question:
    question = models.Question(user_id=questionCreat.userId, content=questionCreat.content,
                               images=[get_question_image_by_id(db, imageid)
                                       for imageid in questionCreat.questionImageids],
                               tags=[get_question_tag_by_id(db, tagid)
                                     for tagid in questionCreat.questionTagids])
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def get_question_by_id(db: Session, id: int) -> models.Question:
    return db.query(models.Question).filter(models.Question.id == id).first()

def delete_question_by_id(db: Session,id: int):
    question = get_question_by_id(db, id)
    db.delete(question)
    db.commit()


def update_question(db: Session, qid: int, questionCreat: schemas.QuestionCreate):
    question = get_question_by_id(db, qid)
    question.content = questionCreat.content
    question.images = [get_question_image_by_id(db, imageid)
                       for imageid in questionCreat.questionImageids]
    question.tags = [get_question_tag_by_id(db, tagid)
                     for tagid in questionCreat.questionTagids]
    db.commit()
    db.refresh(question)
    return question

def set_question_solved(db: Session, qid: int):
    question = get_question_by_id(db, qid)
    question.solved = True
    db.commit()

def get_question_image_by_url(db: Session, url: str) -> models.QuestionImage:
    return db.query(models.QuestionImage).filter(models.QuestionImage.image_url == url).first()


def create_question_image(db: Session, image: schemas.QuestionImageCreate) -> models.QuestionImage:
    question_image = models.QuestionImage(image_url=image.imageUrl,
                                          question=get_question_by_id(db, image.questionId))
    db.add(question_image)
    db.commit()
    db.refresh(question_image)
    return question_image


def get_question_comment_by_id(db, id: int) -> models.QuestionComment:
    return db.query(models.QuestionComment).filter(models.QuestionComment.id == id).first()


def get_question_comment_image_by_url(db: Session, url: str) -> models.QuestionCommentImage:
    return db.query(models.QuestionCommentImage).filter(models.QuestionCommentImage.image_url == url).first()


def get_question_comment_image_by_id(db: Session, id: int) -> models.QuestionCommentImage:
    return db.query(models.QuestionCommentImage).filter(models.QuestionCommentImage.id == id).first()


def create_question_comment_image(db: Session, image: schemas.QuestionCommentImageCreate) -> models.QuestionImage:
    question_image = models.QuestionCommentImage(image_url=image.imageUrl,
                                                 question_comment=get_question_comment_by_id(db,
                                                                                             image.questionCommentId))
    db.add(question_image)
    db.commit()
    db.refresh(question_image)
    return question_image

def delete_question_comment_by_id(db: Session,id: int):
    comment = get_question_comment_by_id(db, id)
    db.delete(comment)
    db.commit()


def search_question_by_word_list(db: Session, word_list: List[str], offset: int, limit: int, asc: int):
    return (db.query(models.Question)
            .filter(or_(*[models.Question.content.like(f"%{word}%") for word in word_list]))
            .order_by(
        models.Question.create_at.desc() if asc == 2 else desc(models.Question.liked_user_count) if asc == 3 else
        models.Question.create_at.desc())
            .offset(offset).limit(limit).all())


def get_search_question_sum_by_word_list(db: Session, word_list: List[str], offset: int, limit: int, asc: int):
    return len(
        (db.query(models.Question)
         .filter(or_(*[models.Question.content.like(f"%{word}%") for word in word_list]))
         .order_by(
            models.Question.create_at.desc() if asc == 2 else desc(models.Question.liked_user_count) if asc == 3 else
            models.Question.create_at.desc()).all())
    )

def get_questions_by_email(db: Session, email: str) -> List[models.Question]:
    user = get_user_by_email(db, email)

    return db.query(models.Question).filter(models.Question.user_id == user.id).all()


def create_question_comment(db: Session, questionCommentCreat: schemas.QuestionCommentCreat) -> models.QuestionComment:
    comment = models.QuestionComment(user_id=questionCommentCreat.userId,
                                     question=get_question_by_id(db, questionCommentCreat.questionId),
                                     content=questionCommentCreat.content,
                                     images=[get_question_comment_image_by_id(db, imageid)
                                             for imageid in questionCommentCreat.questionCommentImageids])
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def update_question_comment(db: Session, question_comment_id: int,
                            comment_create: schemas.QuestionCommentCreat):
    comment = get_question_comment_by_id(db, question_comment_id)
    comment.content = comment_create.content
    comment.images = [get_question_comment_image_by_id(db, imageid)
                      for imageid in comment_create.questionCommentImageids]
    db.commit()
    db.refresh(comment)
    return comment


def set_ans_accept(db: Session, is_accepted: bool, question_comment_id: int):
    comment = get_question_comment_by_id(db, question_comment_id)
    comment.accepted = is_accepted
    db.commit()
    db.refresh(comment)
    if db.query(models.QuestionComment) \
            .filter(models.QuestionComment.question_id == comment.question_id
                    and models.QuestionComment.accepted == True).first():
        comment.question.solved = True
    else:
        comment.question.solved = False
    db.commit()
    return comment


def set_like_question(db: Session, user_id: int, question_id: int, is_like: bool):
    question = get_question_by_id(db, question_id)
    user = get_user_by_id(db, user_id)
    if is_like:
        if user not in question.liked_users:
            question.liked_users.append(user)
            db.commit()
    else:
        if user in question.liked_users:
            question.liked_users.remove(user)
            db.commit()


def set_like_question_comment(db: Session, user_id: int, question_comment_id: int, is_like: bool):
    comment = get_question_comment_by_id(db, question_comment_id)
    user = get_user_by_id(db, user_id)
    if is_like:
        if user not in comment.liked_users:
            comment.liked_users.append(user)
            db.commit()
    else:
        if user in comment.liked_users:
            comment.liked_users.remove(user)
            db.commit()


def get_conversation(db: Session, host_user_id: int, guest_user_id: int):
    return db.query(Conversation).filter(
        and_(Conversation.host_user_id == host_user_id, Conversation.guest_user_id == guest_user_id)).first()


def create_conversation(db: Session, host_user_id: int, guest_user_id: int):
    db_conversation = Conversation(host_user_id=host_user_id, guest_user_id=guest_user_id)
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation


def get_recent_conversation(db: Session, user_id: int):
    return db.query(Conversation).filter(Conversation.host_user_id == user_id).order_by(
        Conversation.update_at.desc()).all()


def create_message(db: Session, sender_id: int, receiver_id: int, content: str):
    db_message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def create_conversation_message(db: Session, conversation_id: int, message_id: int):
    db_conversation_message = models.ConversationMessage(conversation_id=conversation_id, message_id=message_id)
    db.add(db_conversation_message)
    db.commit()
    db.refresh(db_conversation_message)
    return db_conversation_message


def send_message(db: Session, host_user_id: int, guest_user_id: int, content: str):
    db_host_conversation = get_conversation(db, host_user_id, guest_user_id)
    if (host_user_id != guest_user_id):
        db_guest_conversation = get_conversation(db, guest_user_id, host_user_id)
    if db_host_conversation == None:
        db_host_conversation = create_conversation(db, host_user_id, guest_user_id)
        if (host_user_id != guest_user_id):
            db_guest_conversation = create_conversation(db, guest_user_id, host_user_id)
    db_message = create_message(db, sender_id=host_user_id, receiver_id=guest_user_id, content=content)
    try:
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        db_host_conversation.update_at = db_message.create_at
        db_host_conversation.is_read = True
        db.add(db_host_conversation)
        db_assoiation = ConversationMessage(is_read=True, message_id=db_message.id,
                                            conversation_id=db_host_conversation.id)
        db.add(db_assoiation)
        if (host_user_id != guest_user_id):
            db_guest_conversation.update_at = db_message.create_at
            db_guest_conversation.is_read = False
            db.add(db_guest_conversation)
            db_assoiation = ConversationMessage(is_read=False, message_id=db_message.id,
                                                conversation_id=db_guest_conversation.id)
            db.add(db_assoiation)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        return False
