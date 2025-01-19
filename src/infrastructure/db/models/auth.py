import uuid

from peewee import Model, UUIDField, TextField, TimestampField

from ..database import db

#Model representa una tabla dentro de la base de datos. Cada instancia de la clase corresponde a una fila.
class Auth(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)  # Identificador unico
    refresh_token = TextField(null=False)  # Almacena el Token de refresco
    user_id = UUIDField(null=False)  # id de usuario asociado al que pertenece el token.
    emited_date = TimestampField(null =False)   #Fecha de emision del token.
    expired_date = TimestampField(null=False)  # Fecha de expiracion del token
    update_date = TimestampField(null=False)  # Fecha de actualizacion del token

    class Meta:
        database = db
        table_name = 'auth'
