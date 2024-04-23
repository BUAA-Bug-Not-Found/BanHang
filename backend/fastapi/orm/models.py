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
    privilege = Column(Integer, default=0) # 0: 校外User， 1:校内认证User， 2:admin
    userAvatarURL = Column(String(256), nullable=True)

class CheckCode(Base):
    __tablename__ = "checkcode"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(128), nullable=False)
    checkcode = Column(Integer)
    create_at = Column(DateTime, default=datetime.datetime.now)

class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id')) # 实际的数据库关系是通过外键来维护的
    is_anonymous = Column(Boolean, default=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)
    # content_image = Column(String, nullable=True)  # 可以存储图片的路径
    status = Column(Enum('normal', 'archived', 'deleted', name='post_status'), default='normal')
    create_at = Column(DateTime, server_default=func.now()) # 根据服务器时间自动生成

    images = relationship("BlogImage", back_populates="blog")


class BlogImage(Base):
    __tablename__ = 'blog_images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    blog_id = Column(Integer, ForeignKey('blogs.id'))
    image_url = Column(String, nullable=False)
    create_at = Column(DateTime, server_default=func.now()) # 根据服务器时间自动生成
    
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
    create_at = Column(DateTime, server_default=func.now()) # 根据服务器时间自动生成

