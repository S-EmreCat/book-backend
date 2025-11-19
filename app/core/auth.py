from app.helpers.secret_helper import secret_helper
from app.models import AdminUser, User
from app.schemas.admin.auth import AdminLoginOut
from app.schemas.panel.auth import PanelLoginOut


class AuthCore:
    def __init__(self) -> None:
        pass

    def get_token(self, email: str) -> str:
        return secret_helper.create_access_token({"email": email})

    def admin_user_login(self, admin_user: AdminUser) -> AdminLoginOut:
        token = self.get_token(email=admin_user.email)
        return AdminLoginOut(access_token=token)

    def user_login(self, user: User) -> PanelLoginOut:
        token = self.get_token(email=user.email)
        return PanelLoginOut(access_token=token)


auth_core = AuthCore()
