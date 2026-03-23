from peewee import *

db = SqliteDatabase('database.db')

class User(Model):
    id_ = IntegerField()
    balance = IntegerField()

    class Meta:
        database = db # This model uses the "people.db" database.

User.create_table()

class DataBase:
    def GetUser(id_):
        return User.get(User.id_==id_)
        

    def AddUser(id_):
        x = User(id_=id_,
                 balance=50)
        x.save()
        return x

