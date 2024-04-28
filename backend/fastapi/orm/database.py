from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base

import os

current_work_dir = os.path.dirname(__file__)

# 如果在服务器运行，可以通过设置该环境变量确认保存的位置，如果没有设置则在fastapi目录下创建一个。
# 目前支持pg和sqllite
if os.getenv("BANHANG_TEST") is not None:
    dbPath = '{}/../my_database_test.db'.format(current_work_dir)
    SQLALCHEMY_DATABASE_URL = "sqlite:///{}".format(dbPath)
elif os.getenv("BANHANG_DATABASE_PATH") is not None:
    SQLALCHEMY_DATABASE_URL = os.getenv("BANHANG_DATABASE_PATH")
    dbPath = os.getenv("BANHANG_DATABASE_PATH")
else:
    dbPath = '{}/../my_database.db'.format(current_work_dir)
    SQLALCHEMY_DATABASE_URL = "sqlite:///{}".format(dbPath)

Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL) if SQLALCHEMY_DATABASE_URL.startswith("postgresql") else \
    create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# def db_init():
#     Base.metadata.create_all(bind=engine)
#
#
# def db_test():
#     try:
#         with engine.connect() as connection:
#             print("Successfully connected to the database!")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#     db_init()
#     inspector = inspect(engine)
#     tables = inspector.get_table_names()
#     if 'users' in tables:
#         print("The 'users' table exists.")
#     else:
#         print("The 'users' table does not exist.")
