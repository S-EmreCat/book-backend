from app.helpers.secret_helper import secret_helper
from app.models import PanelUser
from app.schemas.admin.auth import LoginOut


class AuthCore:
    def __init__(self):
        pass

    def get_token(self, email: str) -> tuple[str]:
        return secret_helper.create_access_token({"email": email})

    def panel_user_login(self, panel_user: PanelUser):
        token = self.get_token(email=panel_user.email)
        return LoginOut(access_token=token)


auth_core = AuthCore()
