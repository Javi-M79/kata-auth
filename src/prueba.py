from core.services.auth_service import AuthService
from infrastructure.db.database import db
from infrastructure.db.models.auth_model import AuthModel


mail ="javier@mail.com"
password ="1234"

mail = mail.strip()
password = password.strip()

valid_sing = AuthService.generate_sign(mail, password)
print(f"Firma esperada: {valid_sing}")


