import datetime
import os
from typing import List, Type, Dict

from fastapi import  BackgroundTasks
from sqlalchemy.orm import Session, aliased
from orm import models, schemas
from sqlalchemy import or_, and_, desc, func, case, distinct, exists

from orm.database import SessionLocal
from orm.models import Message, Conversation, ConversationMessage, User


def get_user_by_id(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def search_user_by_word(db: Session, word: str, offset: int, limit: int) -> list[Type[User]]:
    return (db.query(models.User)
            .filter(or_(*[models.User.username.like(f"%{word}%")]))
            .order_by(models.User.create_at.asc())
            .offset(offset).limit(limit).all())


def get_search_user_sum_by_word(db: Session, word: str, offset: int, limit: int):
    return len((db.query(models.User)
                .filter(or_(*[models.User.username.like(f"%{word}%")],
                            *[models.User.email.like(f"%{word}%")]))
                .order_by(models.User.create_at.asc()).all()))


# 引入 https://source.boringavatars.com 作为用户默认头像
def create_user(db: Session, user: schemas.UserCreate):
    userAvatarURL = "https://source.boringavatars.com/beam/500/" + user.username + "?square"
    db_user = models.User(username=user.username, password=user.password, email=user.email, userAvatarURL=userAvatarURL)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def set_user_head_url_by_email(db: Session, email: str, url): # todo deprecated
    user = get_user_by_email(db, email)
    user.userAvatarURL = url
    db.commit()
    db.refresh(user)
    return user

def set_user_head_url_by_id(db: Session, id: int, url): # todo deprecated
    user = get_user_by_id(db, id)
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


def set_sign_by_email(db: Session, email: str, sign: str): # todo deprecated
    user = get_user_by_email(db, email)
    user.sign = sign
    db.commit()
    db.refresh(user)
    return user

def set_sign_by_id(db: Session, id: int, sign: str):
    user = get_user_by_id(db, id)
    user.sign = sign
    db.commit()
    db.refresh(user)
    return user


def set_username_by_email(db: Session, email: str, username: str): # todo deprecated
    user = get_user_by_email(db, email)
    user.username = username
    db.commit()
    db.refresh(user)
    return user

def set_username_by_id(db: Session, id: int, username: str):
    user = get_user_by_id(db, id)
    user.username = username
    db.commit()
    db.refresh(user)
    return user


def set_star_state_by_email(db: Session, email1: str, email2: str, is_followed: bool): # todo deprecated
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

def set_star_state_by_user_id(db: Session, id1: int, id2: int, is_followed: bool):
    user1 = get_user_by_id(db, id1)
    user2 = get_user_by_id(db, id2)
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


def get_user_anony_info_by_blog_id(db: Session, blog_id: int, user_id: int, create: bool = False):
    anony_info = (db.query(models.BlogUserAnonyInfo)
                  .filter(models.BlogUserAnonyInfo.blog_id == blog_id, models.BlogUserAnonyInfo.user_id == user_id)
                  .first())

    def random_hex(length):
        import random
        return random.randint(0, 16 ** length)

    if create and anony_info == None:
        try:
            anony_info = models.BlogUserAnonyInfo(blog_id=blog_id, user_id=user_id,
                                                  anony_name=f"匿名用户 #{random_hex(6):06X}",
                                                  anony_avatar_url="https://cdn.icon-icons.com/icons2/1378/PNG/512/avatardefault_92824.png")
            db.add(anony_info)
            db.commit()
            db.refresh(anony_info)
        except Exception as e:
            db.rollback()
    return anony_info


def get_blog_by_blog_id(db: Session, blog_id: int):
    return (db.query(models.Blog)
            .filter(models.Blog.id == blog_id).first())

# 未更新 deleted 相关内容，被鹿哥调用
def get_blog_by_email(db: Session, email: str): # todo deprecated
    user = get_user_by_email(db, email)
    return db.query(models.Blog).filter(models.Blog.user_id == user.id).all()

def get_blogs_by_user_id(db: Session, id: int, not_deleted: bool = False):
    user = get_user_by_id(db, id)
    return (db.query(models.Blog)
            .filter(or_(not_deleted == False, models.Blog.status != "deleted"))
            .filter(models.Blog.user_id == user.id).all())


def get_blogs(db: Session, offset: int = 0, limit: int = 10, asc: bool = False, not_deleted: bool = False):
    return (db.query(models.Blog)
            .filter(or_(not_deleted == False, models.Blog.status != "deleted"))
            .order_by(models.Blog.create_at.asc() if asc else models.Blog.create_at.desc())
            .offset(offset).limit(limit).all())


def get_blogs_by_tag_id(db: Session, blog_tag_id: int, offset: int = 0, limit: int = 10, asc: bool = False, not_deleted: bool = False):
    return (db.query(models.Blog)
            .filter(or_(not_deleted == False, models.Blog.status != "deleted"))
            .join(models.BlogTag, models.Blog.tags)
            .filter(models.BlogTag.id == blog_tag_id)
            .order_by(models.Blog.create_at.asc() if asc else models.Blog.create_at.desc())
            .offset(offset).limit(limit).all())


def get_blogs_by_search_content(db: Session, search_content: str, offset: int, limit: int, asc: int, not_deleted: bool = False):
    word_list = [x.strip() for x in search_content.split(" ") if x != ""]
    return (db.query(models.Blog)
            .filter(or_(not_deleted == False, models.Blog.status != "deleted"))
            .filter(
            or_(*[or_(models.Blog.content.like(f"%{word}%"), models.Blog.title.like(f"%{word}%")) for word in word_list]))
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


def get_blog_tag_by_id(db: Session, tag_id: int):
    return (db.query(models.BlogTag).filter(models.BlogTag.id == tag_id).first())


def get_questions(db: Session, offset: int = 0, limit: int = 10, asc: bool = False, input_user_id: int = 1):
    uqlike = aliased(models.UserQuestionLike)
    if asc:
        # return db.query(models.Question, ).order_by(models.Question.create_at.asc()).offset(offset).limit(limit).all()
        return (db.query(func.max(models.Question.id).label("question_id"),
                         func.max(models.User.id).label("user_id"),
                         func.max(models.User.username).label("user_name"),
                         func.max(models.Question.content).label("question_content"),
                         models.Question.delated.label('question_delated'),
                         models.Question.archived.label('question_archived'),
                         models.Question.solved.label('question_solved'),
                         models.Question.create_at.label('question_create_at'),
                         case((func.count(models.UserQuestionLike.user_id) > 0, True), else_=False).label(
                             'if_user_like'),
                         func.count(distinct(models.QuestionComment.id)).label('ans_sum'),
                         func.count(distinct(uqlike.user_id)).label('like_sum'),
                         )
                .outerjoin(models.QuestionComment, (models.Question.id == models.QuestionComment.question_id))
                .outerjoin(models.UserQuestionLike, ((models.UserQuestionLike.user_id == input_user_id) &
                                                     (models.UserQuestionLike.question_id == models.Question.id)))
                .outerjoin(uqlike, (uqlike.question_id == models.Question.id))
                .filter(models.Question.user_id == models.User.id)
                .group_by(models.Question.id, models.Question.delated, models.Question.archived)
                ).order_by(models.Question.create_at.asc()).offset(offset).limit(limit)
    else:
        # return db.query(models.Question).order_by(models.Question.create_at.desc()).offset(offset).limit(limit).all()
        return (db.query(func.max(models.Question.id).label("question_id"),
                         func.max(models.User.id).label("user_id"),
                         func.max(models.User.username).label("user_name"),
                         func.max(models.Question.content).label("question_content"),
                         models.Question.delated.label('question_delated'),
                         models.Question.archived.label('question_archived'),
                         models.Question.solved.label('question_solved'),
                         models.Question.create_at.label('question_create_at'),
                         case((func.count(models.UserQuestionLike.user_id) > 0, True), else_=False).label(
                             'if_user_like'),
                         func.count(distinct(models.QuestionComment.id)).label('ans_sum'),
                         func.count(distinct(uqlike.user_id)).label('like_sum'),
                         )
                .outerjoin(models.QuestionComment, (models.Question.id == models.QuestionComment.question_id))
                .outerjoin(models.UserQuestionLike, ((models.UserQuestionLike.user_id == input_user_id) &
                                                     (models.UserQuestionLike.question_id == models.Question.id)))
                .outerjoin(uqlike, (uqlike.question_id == models.Question.id))
                .filter(models.Question.user_id == models.User.id)
                .group_by(models.Question.id,
                          models.Question.delated,
                          models.Question.archived,
                          models.Question.solved,
                          models.Question.create_at)
                ).order_by(models.Question.create_at.desc()).offset(offset).limit(limit)


def get_questions_tags(db: Session, question_ids: List[int]) -> Dict[int, List[int]]:
    """
    return {questionid: [tags]}
    """
    res = {}
    if len(question_ids) == 0:
        return res
    for qid in question_ids:
        res[qid] = []
    ret: List[models.QuestionQuestionTag] = (
        db.query(models.QuestionQuestionTag).filter(
            or_(*[(models.QuestionQuestionTag.question_id == qid) for qid in question_ids])).all())
    for qtag in ret:
        res[qtag.question_id].append(qtag.question_tag_id)
    return res


def get_questions_images_urls(db: Session, question_ids: List[int]) -> Dict[int, List[str]]:
    """
    return {questionid: [image_urls]}
    """
    res = {}
    if len(question_ids) == 0:
        return res
    for qid in question_ids:
        res[qid] = []
    ret = (db.query(models.Question.id.label('qid'), models.QuestionImage.image_url.label("image_url"))
           .filter(or_(*[(models.Question.id == qid) for qid in question_ids]))
           .filter(models.Question.id == models.QuestionImage.question_id).all())
    for qimage in ret:
        res[qimage.qid].append(qimage.image_url)
    return res


def get_questions_by_tag(db: Session, offset: int = 0, limit: int = 10, asc: bool = False,
                         tag=None, input_user_id: int = 1):
    uqlike = aliased(models.UserQuestionLike)
    questions = (db.query(func.max(models.Question.id).label("question_id"),
                          func.max(models.User.id).label("user_id"),
                          func.max(models.User.username).label("user_name"),
                          func.max(models.Question.content).label("question_content"),
                          models.Question.delated.label('question_delated'),
                          models.Question.archived.label('question_archived'),
                          models.Question.solved.label('question_solved'),
                          models.Question.create_at.label('question_create_at'),
                          case((func.count(models.UserQuestionLike.user_id) > 0, True), else_=False).label(
                              'if_user_like'),
                          func.count(distinct(models.QuestionComment.id)).label('ans_sum'),
                          func.count(distinct(uqlike.user_id)).label('like_sum'),
                          )
                 .outerjoin(models.QuestionComment, (models.Question.id == models.QuestionComment.question_id))
                 .outerjoin(models.UserQuestionLike, ((models.UserQuestionLike.user_id == input_user_id) &
                                                      (models.UserQuestionLike.question_id == models.Question.id)))
                 .outerjoin(uqlike, (uqlike.question_id == models.Question.id))
                 .filter(models.Question.user_id == models.User.id)
                 .filter(exists().where((models.QuestionQuestionTag.question_id == models.Question.id) &
                                        (models.QuestionQuestionTag.question_tag_id == tag.id)))
                 .group_by(models.Question.id, models.Question.delated, models.Question.archived)
                 ).all()
    if asc:
        return sorted(questions, key=lambda q: q.question_create_at)[offset:offset + limit]
    else:
        return sorted(questions, key=lambda q: q.question_create_at)[offset:offset + limit]


def get_question_sum_by_tag_id(db: Session, tagId):
    return len(db.query(models.QuestionTag).filter(models.QuestionTag.id == tagId).first().questions)


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


def get_question_tag_by_id(db: Session, id: int) -> models.QuestionTag:
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


def delete_question_by_id(db: Session, id: int):
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


def delete_question_comment_by_id(db: Session, id: int):
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


def get_questions_by_email(db: Session, email: str) -> List[models.Question]: # todo deprecated
    user = get_user_by_email(db, email)
    return db.query(models.Question).filter(models.Question.user_id == user.id).all()

def get_questions_by_user_id(db: Session, id: int) -> List[models.Question]:
    user = get_user_by_id(db, id)
    return db.query(models.Question).filter(models.Question.user_id == user.id).all()


def create_question_comment(db: Session, questionCommentCreat: schemas.QuestionCommentCreat,
                            background_tasks: BackgroundTasks) -> models.QuestionComment:
    comment = models.QuestionComment(user_id=questionCommentCreat.userId,
                                     question=get_question_by_id(db, questionCommentCreat.questionId),
                                     content=questionCommentCreat.content,
                                     images=[get_question_comment_image_by_id(db, imageid)
                                             for imageid in questionCommentCreat.questionCommentImageids])
    db.add(comment)
    db.commit()
    db.refresh(comment)
    if os.getenv("BANHANG_TEST") is None:
        background_tasks.add_task(send_message_for_question_answer, comment.id)
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


def set_like_question(db: Session, user_id: int, question_id: int, is_like: bool,
                            background_tasks: BackgroundTasks):
    question = get_question_by_id(db, question_id)
    user = get_user_by_id(db, user_id)
    if is_like:
        if user not in question.liked_users:
            question.liked_users.append(user)
            db.commit()
            if os.getenv("BANHANG_TEST") is None:
                background_tasks.add_task(send_message_for_like_question, question_id, user_id)
    else:
        if user in question.liked_users:
            question.liked_users.remove(user)
            db.commit()


def set_like_question_comment(db: Session, user_id: int, question_comment_id: int, is_like: bool,
                            background_tasks: BackgroundTasks):
    comment = get_question_comment_by_id(db, question_comment_id)
    user = get_user_by_id(db, user_id)
    if is_like:
        if user not in comment.liked_users:
            comment.liked_users.append(user)
            db.commit()
            if os.getenv("BANHANG_TEST") is None:
                background_tasks.add_task(send_message_for_like_question_comment, question_comment_id, user_id)
    else:
        if user in comment.liked_users:
            comment.liked_users.remove(user)
            db.commit()


def get_conversation(db: Session, host_user_id: int, guest_user_id: int):
    return db.query(Conversation).filter(
        and_(Conversation.host_user_id == host_user_id, Conversation.guest_user_id == guest_user_id)).first()

def send_message_for_question_answer(comment_id: int):
    print("back_send_message_for_answer: {}".format(comment_id))
    db = SessionLocal()
    try:
        comment = get_question_comment_by_id(db, comment_id)
        target_user_id = comment.question.user_id
        send_message(db, 34, target_user_id,
                     "自动提示：【{}】 回答了您提出的“{}”问题： {}".format(comment.user.username,
                                                                       comment.question.content,
                                                                       comment.content))
    finally:
        db.close()

def send_message_for_like_question_comment(comment_id: int, like_user:int):
    print("back_send_message_for {} like_answer {}".format(like_user, comment_id))
    db = SessionLocal()
    try:
        comment = get_question_comment_by_id(db, comment_id)
        user = get_user_by_id(db, like_user)
        send_message(db, 34, comment.user_id,
                     "自动提示：【{}】 点赞了您在 “{}” 问题下的回答：“{}”".format(
                         user.username, comment.question.content, comment.content))
    finally:
        db.close()

def send_message_for_like_question(question_id: int, like_user:int):
    print("back_send_message_for {} like_question {}".format(like_user, question_id))
    db = SessionLocal()
    try:
        question = get_question_by_id(db, question_id)
        user = get_user_by_id(db, like_user)
        send_message(db, 34, question.user_id,
                     "自动提示：【{}】 点赞了您提出问题：“{}”".format(user.username, question.content))
    finally:
        db.close()


def get_unread_message_num(db: Session, user_id: int):
    return db.query(func.sum(Conversation.unread_message_num)).filter(Conversation.host_user_id == user_id).scalar()


def create_conversation(db: Session, host_user_id: int, guest_user_id: int):
    db_conversation = Conversation(host_user_id=host_user_id, guest_user_id=guest_user_id)
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation


def get_recent_conversation(db: Session, user_id: int):
    return db.query(Conversation).filter(Conversation.host_user_id == user_id).order_by(
        Conversation.update_at.desc()).all()


def send_message(db: Session, host_user_id: int, guest_user_id: int, content: str):
    if host_user_id == guest_user_id:
        return False
    try:
        db_host_conversation = db.query(Conversation).filter(and_(Conversation.host_user_id == host_user_id,
                                                                  Conversation.guest_user_id == guest_user_id)).with_for_update().first()
        db_guest_conversation = db.query(Conversation).filter(and_(Conversation.host_user_id == guest_user_id,
                                                                   Conversation.guest_user_id == host_user_id)).with_for_update().first()
        if db_host_conversation == None:
            db_host_conversation = Conversation(host_user_id=host_user_id, guest_user_id=guest_user_id)
            db_guest_conversation = Conversation(host_user_id=guest_user_id, guest_user_id=host_user_id)
            db.add(db_host_conversation)
            db.add(db_guest_conversation)
        db.commit()
    except Exception as e:
        db.rollback()
        return False
    try:
        db_message = Message(sender_id=host_user_id, receiver_id=guest_user_id, content=content)
        db.add(db_message)
        db.flush()
        db_host_conversation.update_at = db_message.create_at
        db_host_conversation.is_read = True
        db.add(db_host_conversation)
        db_assoiation = ConversationMessage(is_read=True, message_id=db_message.id,
                                            conversation_id=db_host_conversation.id)
        db.add(db_assoiation)
        db_guest_conversation.update_at = db_message.create_at
        db_guest_conversation.unread_message_num = db_guest_conversation.unread_message_num + 1
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
