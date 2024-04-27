import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from orm.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), unique=True, index=True, nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(256), nullable=False)
    privilege = Column(Integer, default=0)  # 0: 校外User， 1:校内认证User， 2:admin
    userAvatarURL = Column(String(256), nullable=True)

    blogs = relationship("Blog", back_populates="user")
    blog_comments = relationship("BlogComment", back_populates="user")
    questions = relationship("Question", back_populates="user")
    question_comments = relationship("QuestionComment", back_populates="user")
    liked_question_comments = relationship("QuestionComment", secondary="user_question_comment_likes",
                                           back_populates="liked_users")
    liked_questions = relationship("Question", secondary="user_question_likes",
                                   back_populates="liked_users")


class CheckCode(Base):
    __tablename__ = "checkcode"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(128), nullable=False)
    checkcode = Column(Integer)
    create_at = Column(DateTime, default=datetime.datetime.now)


class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # 实际的数据库关系是通过外键来维护的
    is_anonymous = Column(Boolean, default=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)
    # content_image = Column(String, nullable=True)  # 可以存储图片的路径
    status = Column(Enum('normal', 'archived', 'deleted', name='post_status'), default='normal')
    create_at = Column(DateTime, server_default=func.now())  # 根据服务器时间自动生成

    images = relationship("BlogImage", back_populates="blog")
    user = relationship("User", back_populates="blogs")
    comments = relationship("BlogComment", back_populates="blog")
    tags = relationship("BlogTag", secondary="blog_blog_tags", back_populates="blogs")


class BlogImage(Base):
    __tablename__ = 'blog_images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    blog_id = Column(Integer, ForeignKey('blogs.id'))
    image_url = Column(String, nullable=False)
    create_at = Column(DateTime, server_default=func.now())  # 根据服务器时间自动生成

    blog = relationship("Blog", back_populates="images")


class BlogComment(Base):
    __tablename__ = 'blog_comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    blog_id = Column(Integer, ForeignKey('blogs.id'))
    is_anonymous = Column(Boolean, default=False)
    content = Column(String, nullable=True)
    # content_image = Column(String, nullable=True)  # 可以存储图片的路径
    status = Column(Enum('normal', 'archived', 'deleted', name='post_status'), default='normal')
    create_at = Column(DateTime, server_default=func.now())  # 根据服务器时间自动生成
    reply_to_comment_id = Column(Integer, ForeignKey('blog_comments.id'), nullable=True)

    user = relationship("User", back_populates="blog_comments")
    blog = relationship("Blog", back_populates="comments")

    parent = relationship('BlogComment', remote_side=[id], back_populates='replies')
    replies = relationship('BlogComment', back_populates='parent')

class BlogTag(Base):
    __tablename__ = 'blog_tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    blogs = relationship("Blog", secondary="blog_blog_tags", back_populates="tags")

class BlogBlogTag(Base):
    __tablename__ = 'blog_blog_tags'
    blog_id = Column(Integer, ForeignKey('blogs.id'), primary_key=True)
    blog_tag_id = Column(Integer, ForeignKey('blog_tags.id'), primary_key=True)


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String, nullable=True)
    create_at = Column(DateTime, server_default=func.now())
    delated = Column(Boolean, default=False)
    archived = Column(Boolean, default=False)
    solved = Column(Boolean, default=False)


    images = relationship("QuestionImage", back_populates="question")
    comments = relationship("QuestionComment", back_populates="question")
    user = relationship("User", back_populates="questions")
    liked_users = relationship("User", secondary="user_question_likes",
                               back_populates="liked_questions")
    tags = relationship("QuestionTag", secondary="question_question_tags", back_populates="questions")


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

    question = relationship("Question", back_populates="comments")
    user = relationship("User", back_populates="question_comments")
    liked_users = relationship("User", secondary="user_question_comment_likes",
                               back_populates="liked_question_comments")
    images = relationship("QuestionCommentImage", back_populates="question_comment")

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

class QuestionTag(Base):
    __tablename__ = 'question_tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    questions = relationship("Question", secondary="question_question_tags", back_populates="tags")

class QuestionQuestionTag(Base):
    __tablename__ = 'question_question_tags'
    question_id = Column(Integer, ForeignKey('questions.id'), primary_key=True)
    question_tag_id = Column(Integer, ForeignKey('question_tags.id'), primary_key=True)

