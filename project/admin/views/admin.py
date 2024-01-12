from starlette_admin import *

from ._model_view import CustomModelView
from ...db.models import AdminDB

ROLE_CHOICES = (
    ("create", "Creation"),
    ("read", "Read"),
    ("edit", "Editing"),
    ("delete", "Deleting"),
)


class AdminView(CustomModelView):
    """
    View for managing admins table in the admin panel.
    """
    fields = [
        IntegerField(
            AdminDB.id.name, "ID",
            read_only=True,
        ),
        HasOne(
            AdminDB.user.__str__().split(".")[-1], "User",
            identity="user",
            required=True,
        ),
        EnumField(
            AdminDB.roles.name, "Roles",
            choices=ROLE_CHOICES, select2=True, multiple=True
        ),
        DateTimeField(
            AdminDB.created_at.name, "Created at",
            read_only=True,
        ),
    ]
    exclude_fields_from_create = ["created_at"]
    searchable_fields = [c.name for c in AdminDB.__table__.columns]  # type: ignore
