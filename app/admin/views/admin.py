from starlette_admin import *

from ._model_view import MyModelView

ROLE_CHOICES = (
    ("create", "Creation"),
    ("read", "Read"),
    ("edit", "Editing"),
    ("delete", "Deletion"),
)


class AdminView(MyModelView):
    """
    View for managing admins table in the admin panel.
    """
    fields = [
        IntegerField("id", "ID", read_only=True),

        HasOne(
            "user", "User",
            identity="user", required=True,
        ),
        EnumField(
            "roles", "Roles",
            choices=ROLE_CHOICES, select2=True, multiple=True
        ),
        DateTimeField("created_at", "Created at", read_only=True),
    ]
    searchable_fields = ["__all__"]
    exclude_fields_from_create = ["created_at"]
