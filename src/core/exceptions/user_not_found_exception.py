from infrastructure.db.models.user_model import UserModel


class UserNotFoundException(Exception):
    def __init__(self, message="Usuario no encontrado."):
        self.message = message
        super().__init__(self.message)


def search_user(login_data):
    user = UserModel.select().where(UserModel.mail == login_data.mail).first()
    if not user:
        raise UserNotFoundException
    return user
