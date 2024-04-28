import os,sys
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orm.database import engine, SQLALCHEMY_DATABASE_URL
from orm import models

# 如果在服务器运行，可以通过设置环境变量确认保存的位置，如果没有设置则在fastapi目录下创建一个。


# def recreate_sqlite_db(bind_engine = engine):
#     assert is_sqlite_db()
#     if os.path.exists(dbPath):
#         try:
#             os.remove(dbPath)
#         except:
#             raise "can't remove old db on {}".format(dbPath)
#     models.Base.metadata.create_all(bind=bind_engine)

def recreate_pg_db(bind_engine = engine):
    assert is_pg_db()
    models.Base.metadata.drop_all(bind=bind_engine)
    models.Base.metadata.create_all(bind=bind_engine)


def is_pg_db():
    return SQLALCHEMY_DATABASE_URL.startswith("postgresql")

def is_sqlite_db():
    return SQLALCHEMY_DATABASE_URL.startswith("sqlite")

def recreate_db():
    if is_sqlite_db():
        recreate_sqlite_db()
    elif is_pg_db():
        recreate_pg_db()

def upgrade_db():
    models.Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    recreate_db()