from datetime import timedelta
import hashlib
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from domain.entities.user_entity import UserEntity


class AuthService:
    @staticmethod
    def generate_sing():
    #generacion de hash SAH 256 basado en username y password.