import peewee
import datetime

db = peewee.SqliteDatabase('my_database.db')

from peewee import Model, CharField, IntegerField, AutoField

class User(Model):
    uid = AutoField(primary_key=True)
    username = CharField(max_length=32, unique=True)
    password = CharField(max_length=32)

    class Meta:
        database = db
        db_table = 'user'


if __name__ == '__main__':
    User.create_table()