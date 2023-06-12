from peewee import *

db = SqliteDatabase('bot_database.sqlite3')

# model for register user in database
class User(Model):
    user_id = CharField()
    stage = CharField()


    class Meta:
        database = db



