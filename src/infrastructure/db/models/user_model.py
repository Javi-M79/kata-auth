import uuid
from peewee import Model, UUIDField, CharField
from infrastructure.db.database import db


#Esta clase se corresponde con el modelo de la base de datos

class UserModel(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    username = CharField(unique=True, null=False)
    mail = CharField(unique=True, null=False)
    password = CharField(null=False)

    class Meta():
        database = db
        table_name = 'users'
