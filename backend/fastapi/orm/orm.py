import os
import peewee
import datetime

current_work_dir = os.path.dirname(__file__)

# 如果在服务器运行，可以通过设置该环境变量确认保存的位置，如果没有设置则在fastapi目录下创建一个。
if os.getenv("BANHANG_DATABASE_PATH") is not None:
    db = peewee.SqliteDatabase(os.getenv("BANHANG_DATABASE_PATH"))
else:
    db = peewee.SqliteDatabase('{}/../my_database.db'.format(current_work_dir))

from peewee import Model, CharField, IntegerField, AutoField

class User(Model):
    uid = AutoField(primary_key=True)
    username = CharField(max_length=32, unique=True)
    password = CharField(max_length=32)
    admin = peewee.BooleanField(default=False)

    class Meta:
        database = db
        db_table = 'user'

if __name__ == '__main__':
    # 暂时约定执行这部分代码的目的是重新生成整个数据库。
    # 修改模型后，记得在此处建表
    User.create_table()