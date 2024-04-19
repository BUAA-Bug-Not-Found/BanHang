import os
os.environ["BANHANG_TEST"] = "TRUE"
import backend.fastapi.orm.orm as orm
import importlib
import pytest

def regenerate_database():
    importlib.reload(orm)
    orm.generateDB()

@pytest.fixture
def mock_user_data():
    # 提供一个模拟的用户数据
    return {
        "username": "testuser",
        "password": "testpass"
    }

@pytest.fixture
def new_database():
    regenerate_database()