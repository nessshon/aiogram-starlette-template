from starlette_admin.contrib.sqla import Admin

from ._model_view import AdminRoles
from .admin import AdminView
from .user import UserView
from ...db import models


def admin_views_add(admin: Admin) -> None:  # noqa
    """
    Add views to admin panel.
    """
    admin.add_view(AdminView(models.Admin, icon="fas fa-user-tie", identity="admin"))
    admin.add_view(UserView(models.User, icon="fas fa-user", identity="user"))


__all__ = [
    "admin_views_add",
    "AdminRoles"
]
