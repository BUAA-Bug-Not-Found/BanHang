import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum, DateTime, Table, text
from sqlalchemy.orm import relationship, backref, Mapped
from sqlalchemy.sql import func

from orm.database import Base
from typing import Optional, List, Set

user_user_stars = Table(
    'user_user_stars',
    Base.metadata,
    Column('user1', Integer, ForeignKey('users.id')),
    Column('user2', Integer, ForeignKey('users.id'))
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), index=True, nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(256), nullable=False)
    privilege = Column(Integer, nullable=False, default=0)  # 0:校内认证User， 1+:admin
    userAvatarURL = Column(String(256), nullable=False,
                           default="https://banhang.oss-cn-beijing.aliyuncs.com/3bda01f4fce948d88ee72babced0a3c0.png")
    sign = Column(String, nullable=False, default="快来设置个性签名叭~~")
    coin = Column(Integer, nullable=False, server_default=text('1'))
    exp = Column(Integer, nullable=False, server_default=text('0'))
    create_at = Column(DateTime, server_default=func.now())
    last_exp_add_time = Column(DateTime, nullable=False, server_default=func.now())
    today_exp_add_sum = Column(Integer, nullable=False, server_default=text('0'))

    activate_time = Column(DateTime, nullable=True, server_default=func.now())

    blogs = relationship("Blog", back_populates="user")
    blog_comments = relationship("BlogComment", back_populates="user")
    questions = relationship("Question", back_populates="user")
    question_comments = relationship("QuestionComment", back_populates="user")
    liked_question_comments = relationship("QuestionComment", secondary="user_question_comment_likes",
                                           back_populates="liked_users")
    liked_questions = relationship("Question", secondary="user_question_likes",
                                   back_populates="liked_users")
    focused_questions = relationship("Question", secondary="user_question_focuses",
                                     back_populates="focused_users")
    followed = relationship(
        "User",
        secondary=user_user_stars,
        primaryjoin=(user_user_stars.c.user1 == id),
        secondaryjoin=(user_user_stars.c.user2 == id),
        lazy="dynamic",
        backref=backref('followers', lazy='dynamic'))
    # badges = relationship("UserBadge", back_populates="users")
    badges: Mapped[List["Badge"]] = relationship(
        secondary="user_badges", back_populates="owners"
    )


class CheckCode(Base):
    __tablename__ = "checkcode"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(128), nullable=False)
    checkcode = Column(Integer)
    create_at = Column(DateTime, default=datetime.datetime.now)


class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # 实际的数据库关系是通过外键来维护的
    is_anonymous = Column(Boolean, nullable=False, default=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False, default="")
    status = Column(Enum('normal', 'archived', 'deleted', name='post_status'), default='normal')
    create_at = Column(DateTime, nullable=False, server_default=func.now())  # 根据服务器时间自动生成
    reply_at = Column(DateTime, nullable=False, server_default=func.now())

    images = relationship("BlogImage", back_populates="blog")
    user = relationship("User", back_populates="blogs")
    comments = relationship("BlogComment", back_populates="blog")
    tags = relationship("BlogTag", secondary="blog_blog_tags", back_populates="blogs")

    reported_issues = relationship("ReportedIssue", back_populates="blog")


class BlogImage(Base):
    __tablename__ = 'blog_images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    blog_id = Column(Integer, ForeignKey('blogs.id'), nullable=False)
    image_url = Column(String, nullable=False)
    create_at = Column(DateTime, nullable=False, server_default=func.now())  # 根据服务器时间自动生成

    blog = relationship("Blog", back_populates="images")


class BlogComment(Base):
    __tablename__ = 'blog_comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    blog_id = Column(Integer, ForeignKey('blogs.id'), nullable=False)
    is_anonymous = Column(Boolean, default=False, nullable=False)
    content = Column(String, nullable=False, default="")
    status = Column(Enum('normal', 'archived', 'deleted', name='post_status'), default='normal')
    create_at = Column(DateTime, nullable=False, server_default=func.now())  # 根据服务器时间自动生成
    reply_to_comment_id = Column(Integer, ForeignKey('blog_comments.id'), nullable=True)

    user = relationship("User", back_populates="blog_comments")
    blog = relationship("Blog", back_populates="comments")

    comments: Mapped[List["BlogComment"]] = relationship(back_populates="reply_to_comment")
    reply_to_comment: Mapped[Optional["BlogComment"]] = relationship(back_populates="comments", remote_side=id)

    reported_issues = relationship("ReportedIssue", back_populates="blog_comment")


class BlogTag(Base):
    __tablename__ = 'blog_tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    icon = Column(String, nullable=False, default='tagIcon')
    color = Column(String, nullable=False, default='blue-darken-1')
    blogs = relationship("Blog", secondary="blog_blog_tags", back_populates="tags")


class BlogBlogTag(Base):
    __tablename__ = 'blog_blog_tags'
    blog_id = Column(Integer, ForeignKey('blogs.id'), primary_key=True)
    blog_tag_id = Column(Integer, ForeignKey('blog_tags.id'), primary_key=True)


class BlogUserAnonyInfo(Base):
    __tablename__ = 'blog_user_anony_info'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    blog_id = Column(Integer, ForeignKey('blogs.id'), primary_key=True)
    anony_id = Column(Integer, ForeignKey('anony_infos.id'), nullable=True, default=None)
    anony_name = Column(String, nullable=True)
    anony_avatar_url = Column(String, nullable=True)

    def __init__(self, blog_id: int, user_id: int, anony_id: int = None, anony_name: str = "匿名用户", anony_avatar_url: str = "https://cdn.icon-icons.com/icons2/1378/PNG/512/avatardefault_92824.png"):
        self.user_id = user_id
        self.blog_id = blog_id
        self.anony_id = anony_id
        self.anony_name = anony_name
        self.anony_avatar_url = anony_avatar_url


class AnonyInfo(Base):
    __tablename__ = 'anony_infos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    avatar_url = Column(String, nullable=False)


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String, nullable=False, default="")
    create_at = Column(DateTime, server_default=func.now())
    delated = Column(Boolean, default=False)
    archived = Column(Boolean, default=False)
    solved = Column(Boolean, default=False)
    liked_user_count = Column(Integer, default=0, nullable=False)

    images = relationship("QuestionImage", back_populates="question")
    comments = relationship("QuestionComment", back_populates="question")
    user = relationship("User", back_populates="questions")
    liked_users = relationship("User", secondary="user_question_likes",
                               back_populates="liked_questions")
    focused_users = relationship("User", secondary="user_question_focuses",
                                 back_populates="focused_questions")
    tags = relationship("QuestionTag", secondary="question_question_tags", back_populates="questions")

    reported_issues = relationship("ReportedIssue", back_populates="question")


class QuestionImage(Base):
    __tablename__ = 'question_images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    image_url = Column(String, nullable=False)
    create_at = Column(DateTime, server_default=func.now())

    question = relationship("Question", back_populates="images")


class QuestionComment(Base):
    __tablename__ = 'question_comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String)
    create_at = Column(DateTime, server_default=func.now())
    delated = Column(Boolean, default=False)
    accepted = Column(Boolean, default=False)
    reply_comment_id = Column(Integer, ForeignKey('question_comments.id'), nullable=True)

    question = relationship("Question", back_populates="comments")
    user = relationship("User", back_populates="question_comments")
    liked_users = relationship("User", secondary="user_question_comment_likes",
                               back_populates="liked_question_comments")
    images = relationship("QuestionCommentImage", back_populates="question_comment")
    reply_to_comment = relationship("QuestionComment",
                                    foreign_keys=[reply_comment_id],
                                    remote_side=[id],
                                    back_populates="comments")
    comments = relationship("QuestionComment", back_populates="reply_to_comment")
    reported_issues = relationship("ReportedIssue", back_populates="question_comment")


class QuestionCommentImage(Base):
    __tablename__ = 'question_comment_images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_comment_id = Column(Integer, ForeignKey('question_comments.id'))
    image_url = Column(String, nullable=False)
    create_at = Column(DateTime, server_default=func.now())

    question_comment = relationship("QuestionComment", back_populates="images")


class UserQuestionCommentLike(Base):
    __tablename__ = 'user_question_comment_likes'
    question_id = Column(Integer, ForeignKey('question_comments.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)


class UserQuestionLike(Base):
    __tablename__ = 'user_question_likes'
    question_id = Column(Integer, ForeignKey('questions.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)


class UserQuestionFocus(Base):
    __tablename__ = 'user_question_focuses'
    question_id = Column(Integer, ForeignKey('questions.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)


class QuestionTag(Base):
    __tablename__ = 'question_tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    icon = Column(String, nullable=False, default='tagIcon')
    color = Column(String, nullable=False, default='blue-darken-1')
    questions = relationship("Question", secondary="question_question_tags", back_populates="tags")
    is_admin = Column(Boolean, default=False, nullable=False)


class QuestionQuestionTag(Base):
    __tablename__ = 'question_question_tags'
    question_id = Column(Integer, ForeignKey('questions.id'), primary_key=True)
    question_tag_id = Column(Integer, ForeignKey('question_tags.id'), primary_key=True)


class ReportedIssue(Base):
    __tablename__ = 'reported_issue'
    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=True)
    question_comment_id = Column(Integer, ForeignKey('question_comments.id'), nullable=True)
    blog_id = Column(Integer, ForeignKey('blogs.id'), nullable=True)
    blog_comment_id = Column(Integer, ForeignKey('blog_comments.id'), nullable=True)

    user_id = Column(Integer, ForeignKey('users.id'))

    reason = Column(String, nullable=False)
    is_question = Column(Boolean, default=False, nullable=False)
    is_blog = Column(Boolean, default=False, nullable=False)
    is_comment = Column(Boolean, default=False, nullable=False)
    create_at = Column(DateTime, nullable=False, server_default=func.now())

    question = relationship("Question", back_populates="reported_issues")
    question_comment = relationship("QuestionComment", back_populates="reported_issues")
    blog = relationship("Blog", back_populates="reported_issues")
    blog_comment = relationship("BlogComment", back_populates="reported_issues")


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(String, nullable=False, default="")
    create_at = Column(DateTime, nullable=False, server_default=func.now())

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])

    conversation: Mapped["Conversation"] = relationship(
        secondary="conversation_messages", back_populates="messages"
    )


class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    host_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    guest_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_read = Column(Boolean, nullable=False, default=True)
    unread_message_num = Column(Integer, nullable=False, default=0)
    update_at = Column(DateTime, nullable=False, server_default=func.now())

    host_user = relationship("User", foreign_keys=[host_user_id])
    guest_user = relationship("User", foreign_keys=[guest_user_id])

    messages: Mapped[List["Message"]] = relationship(
        secondary="conversation_messages", back_populates="conversation"
    )


class ConversationMessage(Base):
    __tablename__ = 'conversation_messages'
    conversation_id = Column(Integer, ForeignKey('conversations.id'), primary_key=True)
    message_id = Column(Integer, ForeignKey('messages.id'), primary_key=True)
    is_read = Column(Boolean, nullable=False, default=False) # 目前没有使用


class BoyaEntrust(Base):
    __tablename__ = 'boya_entrusts'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    campus = Column(String, nullable=False)
    type = Column(String, nullable=False)


class Badge(Base):
    __tablename__ = 'badges'
    id = Column(Integer, primary_key=True, autoincrement=True)
    creater_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    short_name = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    background_color = Column(String, nullable=False)
    icon_url = Column(String, nullable=False)
    create_at = Column(DateTime, nullable=False, server_default=func.now())  # 根据服务器时间自动生成
    cost = Column(Integer, nullable=False, default=0)

    creater = relationship("User", foreign_keys=[creater_id])
    # users = relationship("UserBadge", back_populates="badges")
    owners: Mapped[List[User]] = relationship(
        secondary="user_badges", back_populates="badges"
    )


class UserBadge(Base):
    __tablename__ = 'user_badges'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    badge_id = Column(Integer, ForeignKey('badges.id'), primary_key=True)
    create_at = Column(DateTime, nullable=False, server_default=func.now())  # 根据服务器时间自动生成
