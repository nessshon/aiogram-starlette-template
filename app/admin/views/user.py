from starlette.requests import Request
from starlette_admin import *

from ._model_view import MyModelView

STATE_CHOICES = (
    ("kicked", "Kicked"),
    ("member", "Member"),
)


class UserView(MyModelView):
    """
    View for managing users table in the admin panel.
    """

    fields = [
        IntegerField("id", "ID", read_only=True),
        IntegerField("user_id", "Telegram ID", read_only=True),

        EnumField(
            "state", "State",
            required=False,
            read_only=True,
            choices=STATE_CHOICES,
            maxlength=6,
        ),
        StringField(
            "first_name", "Name",
            required=True,
            maxlength=64,
        ),
        StringField(
            "username", "Username",
            required=False,
            maxlength=64,
        ),
        DateTimeField("created_at", "Created at", read_only=True),
    ]
    form_include_pk = True
    exclude_fields_from_create = ["created_at"]
    searchable_fields = ["all"]

    def can_create(self, request: Request) -> bool:
        return False
