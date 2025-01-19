import uuid

from peewee import UUIDField, Model, CharField
from ..database import db


class User(Model):
    id = UUIDField(primary_key=True, default= uuid.uuid4)
    username = CharField(unique=True, null = False)
    password = CharField(null = False)

    class Meta():
        database = db
        table_name='user'
