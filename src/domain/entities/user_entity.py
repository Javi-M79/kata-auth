
class UserEntity:
    def __init__(self, user: str, password: str, mail: str, given_name: str = None):
        self.user_name = user
        self.password = password
        self.mail = mail
        self.given_name = given_name
