from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

current_work_dir = os.path.dirname(__file__)

# 如果在服务器运行，可以通过设置该环境变量确认保存的位置，如果没有设置则在fastapi目录下创建一个。
if os.getenv("BANHANG_DATABASE_PATH") is not None:
    dbPath = os.getenv("BANHANG_DATABASE_PATH")
else:
    if os.getenv("BANHANG_TEST") is not None:
        dbPath = '{}/../my_database_test.db'.format(current_work_dir)
    else:
        dbPath = '{}/../my_database.db'.format(current_work_dir)

SQLALCHEMY_DATABASE_URL = "sqlite:///{}".format(dbPath)
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
