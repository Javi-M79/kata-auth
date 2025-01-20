import uuid

from peewee import Model, UUIDField, TextField, TimestampField, ForeignKeyField

from infrastructure.db.database import db
from infrastructure.db.models.user_model import UserModel


#Esta clase se corresponde con el modelo de la base de datos
#Model representa una tabla dentro de la base de datos. Cada instancia de la clase corresponde a una fila.
class AuthModel(Model):

    id = UUIDField(primary_key=True, default=uuid.uuid4)  # Identificador único
    refresh_token = TextField(unique=True, null=False)  # Token de refresco único
    user_id = ForeignKeyField(UserModel, backref="auths", on_delete="CASCADE")  # Relación con usuario
    emit_date = TimestampField(null=False)  # Fecha de emisión
    expired_date = TimestampField(null=False)  # Fecha de expiración
    update_date = TimestampField(null=False)  # Fecha de última actualización

    class Meta:
        database = db
        table_name = 'auth'
