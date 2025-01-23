from core.exceptions.mail_format_exception import MailFormatException
from core.services.auth_service import AuthService

mail ="javiermailcom"
password ="1234"

mail = mail.strip()
password = password.strip()
validate_mail = MailFormatException(mail)
valid_sing = AuthService.generate_sign(mail, password)
print(f"Firma esperada: {valid_sing}")


