import hashlib

#Generamos la firma con correo (identificador principal del usuario y password para permitir usuarios con mismo nombre.
#Revisar com Marck.
class AuthService:
    @staticmethod
    def generate_sing(mail: str, password: str, ) -> str:
    #generacion de hash SAH 256 basado en username y password.
        raw_string = f"{mail},{password}" #Concatena correo y contrasenya
        return hashlib.sha256(raw_string.encode()).hexdigest()#Genera hash en SAH 256

    @staticmethod
    def validate_sing(mail: str, password: str, sing: str) -> None:
        expected_sing = AuthService.generate_sing(mail, password)
        if sing != expected_sing:
            raise ValueError("La firma no es valida")
