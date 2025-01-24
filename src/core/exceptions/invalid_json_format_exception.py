
#Excepcion que asegura que el formato que recibimos sea un JSON valido.
#Uso: comprobar que el request.get_json que recogemos en la variable data funciona correctamente.

class InvalidJsonFormatException(Exception):
    def __init__(self, message:"El cuerpo de la solicitud debe ser un JSON valido."):
        self.message = message
        super().__init__(self.message)