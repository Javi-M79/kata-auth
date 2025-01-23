
#Excepcion de comprobacion del mail introducido por el usuario.

class MailFormatException(Exception):
    # Pasamos el mail por parametro
    def __init__(self):
        super().__init__(f"Formato de correo electronico no valido.")

    @staticmethod
    def validate_mail_format(mail: str):
        # El mail debe tener @ y ".". En caso contrario lanzará una excepcion
        if not "@" in mail or not "." in mail:
            raise MailFormatException()
