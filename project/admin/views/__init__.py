from starlette_admin.contrib.sqla import Admin

from ._model_view import AdminRoles

from .admin import AdminView
from .user import UserView

from ...db import models


def admin_views_add(admin: Admin) -> None:  # noqa
    """
    Add views to admin panel.
    """
    admin.add_view(
        AdminView(
            models.AdminDB,
            icon=models.AdminDB.__admin_icon__,
            label=models.AdminDB.__admin_name__,
            name=models.AdminDB.__admin_label__,
            identity=models.AdminDB.__admin_identity__,
        ),
    )
    admin.add_view(
        UserView(
            models.UserDB,
            icon=models.UserDB.__admin_icon__,
            label=models.UserDB.__admin_label__,
            name=models.UserDB.__admin_name__,
            identity=models.UserDB.__admin_identity__,
        ),
    )


__all__ = [
    "admin_views_add",
    "AdminRoles"
]
