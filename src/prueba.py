from core.services.auth_service import AuthService

mail ="javier@mail.com"
password ="1234"

mail = mail.strip()
password = password.strip()

valid_sing = AuthService.generate_sign(mail, password)
print(f"Firma esperada: {valid_sing}")


