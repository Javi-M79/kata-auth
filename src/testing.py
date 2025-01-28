import hashlib

from flask.cli import load_dotenv

from core.exceptions.mail_format_exception import MailFormatException
from core.services.auth_service import AuthService
import os



load_dotenv()

mail ="javier@mailcom"
password ="1234"

mail = mail.strip()
password = password.strip()

valid_sing = AuthService.generate_sign(mail, password)
print(f"Firma esperada: {valid_sing}")
"""jwt_secret_key = os.getenv('JWT_SECRET_KEY')
raw_jwt_secret_key = jwt_secret_key.encode('utf-8')
encoded_jwt_secret_key = hashlib.sha256(raw_jwt_secret_key).hexdigest()
print(f"Contraseña encriptada: {encoded_jwt_secret_key}")"""

