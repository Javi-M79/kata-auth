class RegisterDTO:
    def __init__(self, username: str, mail: str, password: str):
        """
               DTO para manejar y validar los datos enviados al registro.
               :param username: Nombre de usuario.
               :param mail: Correo electrónico único.
               :param password: Contraseña del usuario.
               :raises ValueError: Si falta algún campo obligatorio.
               """
        if not username or not mail or not password:
            raise ValueError("Faltan campos obligatorios.")
        self.username = username
        self.mail = mail
        self.password = password
