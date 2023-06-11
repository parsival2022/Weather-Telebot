from peewee import *

db = SqliteDatabase('bot_database.sqlite3')

class User(Model):
    user_id = CharField()
    stage = CharField()

    class Meta:
        database = db


# if __name__ == '__main__':
#     db.create_tables([User])

