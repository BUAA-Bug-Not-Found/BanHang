from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from orm.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), unique=True, index=True, nullable=False)
    email = Column(String(64), nullable=True)
    password = Column(String(256), nullable=False)
    privilege = Column(Integer, default=0) # 0: 校外User， 1:校内认证User， 2:admin
