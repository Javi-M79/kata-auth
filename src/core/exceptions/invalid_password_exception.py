class InvalidPasswordException:
    def __init__(self, message:"Usuario o contraseña incorrectos"):
        self.message = message
        super().__init__(self.message)