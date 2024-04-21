import os
from orm.database import dbPath,engine
from orm import models

# 如果在服务器运行，可以通过设置环境变量确认保存的位置，如果没有设置则在fastapi目录下创建一个。


def recreate_sqlite_db(bind_engine = engine):
    # print("\ndatabase recreated")
    if os.path.exists(dbPath):
        try:
            os.remove(dbPath)
        except:
            raise "can't remobe old db on {}".format(dbPath)
    models.Base.metadata.create_all(bind=bind_engine)


def upgrade_sqlite_db():
    models.Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    recreate_sqlite_db()