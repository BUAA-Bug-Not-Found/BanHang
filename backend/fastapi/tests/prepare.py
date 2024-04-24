import os,sys
os.environ["BANHANG_TEST"] = "TRUE"
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
import orm.database as database
from scripts.recreate_db import recreate_sqlite_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app


class database_handler():
    engine = None
    sessionmaker = None
    dbs=[]
    @staticmethod
    def regenerate_database():
        for db in database_handler.dbs:
            db.close()
        if database_handler.engine:
            database_handler.engine.dispose()
        database_handler.engine = create_engine(
            database.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
        )
        recreate_sqlite_db(database_handler.engine)
        database_handler.sessionmaker = sessionmaker(autocommit=False, autoflush=False,
                                                     bind=database_handler.engine)
        database_handler.dbs=[]



def override_get_db():
    # print("get test db")
    try:
        db = database_handler.sessionmaker()
        database_handler.dbs.append(db)
        yield db
    finally:
        db.close()
        database_handler.dbs.remove(db)



app.dependency_overrides[database.get_db] = override_get_db


@pytest.fixture
def mock_user_data():
    # 提供一个模拟的用户数据
    return {
        "username": "testuser",
        "password": "testpass",
        "email": "testemail@test.com",
        "checkCode": "123456"
    }

@pytest.fixture
def mock_blog_data():
    # 提供一个模拟的 Blog 数据
    return {
        "title": "blogTitle",
        "content": "blogContent",
        "ifAnonymous": True,
        "imageList": [
            "string"
        ]
    }

@pytest.fixture
def mock_question_data():
    return {
        'quesContent':{
            'content': 'can you help me???',
            'imageList': []
        },
        'quesTags':['tag1','tag2']
    }

@pytest.fixture
def new_database():
    database_handler.regenerate_database()
