import uuid

from peewee import Model, UUIDField, TextField, TimestampField

from ..database import db


class auth_model(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4())  # Identificador unico
    refresh_token = TextField(null=False)  # Token de refresco
    user_id = UUIDField(null=False)  # id de usuario asociado
    expired_date = TimestampField(null=False)  # Fecha de emision
    update_date = TimestampField(null=False)  # Fecha de actualizacion

    class Meta:
        database = db
        table_name = 'auth'
