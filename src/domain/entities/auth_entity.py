
class AuthEntity:
    def __init__(self, id, refresh_token, user_id, emited_date,expired_date,update_date):
        self.id = id
        self.refresh_token = refresh_token
        self.user_id = user_id
        self.emited_date = emited_date
        self.expired_date = expired_date
        self.update_date = update_date
