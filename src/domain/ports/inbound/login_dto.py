# Valida y estructura los datos enviados en el cuerpo de la solicitud al endpoint /login.
# Garantiza que los datos como mail, password y sign estén presentes.
# Este es el esquema que tendra el JSON  que recibamos al hacer login.

class LoginDTO:
    def __init__(self, mail: str, password, sign: str):
        """
              Inicializa el DTO con los datos del login y valida que estén completos.
              :param mail: Correo electrónico del usuario.
              :param password: Contraseña del usuario.
              :param sign: Firma generada para la solicitud.
              :raises ValueError: Sí falta algún campo obligatorio.              """

        if not mail or not password:
            raise ValueError("Faltan campos obligatorios.")

        self.mail = mail
        self.password = password
        self.sign = sign
