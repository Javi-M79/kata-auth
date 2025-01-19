import hashlib
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta

#Generamos la firma con correo (identificador principal del usuario) y password para permitir usuarios con mismo nombre.
#Revisar com Marck.
class AuthService:
    @staticmethod
    def generate_sing(mail: str, password: str, ) -> str:
    #generacion de hash SAH 256 basado en username y password.
        raw_string = f"{mail},{password}" #Concatena correo y contrasenya
        return hashlib.sha256(raw_string.encode()).hexdigest()#Genera hash en SAH 256

    @staticmethod
    def validate_sign(mail: str, password: str, sign: str) -> None:
        expected_sign = AuthService.generate_sing(mail, password)
        if sign != expected_sign:
            raise ValueError("La firma no es valida")

    # Generacion de Token JWT y refresh Token
    def generate_tokens(user_id:str)->dict:
        access_token = create_access_token(identity=user_id, expires_delta=timedelta(days=2))
        refresh_token = create_refresh_token(identity=user_id, expires_delta=timedelta(weeks=1))
        # Devolver los tokens con datos de usuario

        return{
            "token": access_token,
            "refreshToken": refresh_token

        }