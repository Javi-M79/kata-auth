import hashlib
from datetime import timedelta, datetime
from flask_jwt_extended import create_access_token, create_refresh_token
from peewee import DoesNotExist

from infrastructure.db.models.auth_model import AuthModel


#Generamos la firma con correo (identificador principal del usuario) y password para permitir usuarios con mismo nombre.
#Revisar com Marck.
class AuthService:

    @staticmethod
    def generate_sign(mail: str, password: str, ) -> str:
    #generacion de hash SAH 256 basado en username y password.
        raw_string = f"{mail},{password}" #Concatena correo y contrasenya
        return hashlib.sha256(raw_string.encode()).hexdigest()#Genera hash en SAH 256

    @staticmethod
    def validate_sign(mail: str, password: str, sign: str) -> None:
        expected_sign = AuthService.generate_sign(mail, password)
        if sign != expected_sign:
            raise ValueError("La firma no es valida")

    # Generacion de Token JWT y refresh Token
    @staticmethod
    def generate_tokens(user_id:str)->dict:
        access_token = create_access_token(identity=user_id, expires_delta=timedelta(days=2))
        refresh_token = create_refresh_token(identity=user_id, expires_delta=timedelta(weeks=1))
        # Devolvemos tokens generados
        return{
            "access_token": access_token,
            "refresh_token": refresh_token

        }

    @staticmethod
    def store_refresh_token(user_id: str, refresh_token: str):
        now = datetime.utcnow()
        expiration = now + timedelta(weeks=1) #Fecha de expiracion en una semana.

        AuthModel.create(
            refresh_token=refresh_token,
            user_id=user_id,
            emit_date=now,
            expired_date=expiration,
            update_date=now
        )

    @staticmethod
    def verify_refresh_token(refresh_token: str):
        try:
            token = AuthModel.get(AuthModel.refresh_token == refresh_token)
            if token.expired_date < datetime.utcnow():
                raise ValueError("Token caducado")
            return token
        except DoesNotExist:
            raise ValueError("El token no es valido.")
