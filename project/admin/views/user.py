from starlette.requests import Request
from starlette_admin import *

from ._model_view import CustomModelView
from ...db.models import UserDB

STATE_CHOICES = (
    ("kicked", "Kicked"),
    ("member", "Member"),
)

LANGUAGE_CHOICES = (
    ("ru", "Russian"),
    ("en", "English"),
)


class UserView(CustomModelView):
    """
    View for managing users table in the admin panel.
    """
    fields = [
        IntegerField(
            UserDB.id.name, "Telegram ID",
            read_only=True,
        ),
        EnumField(
            UserDB.state.name, "State",
            required=False,
            read_only=True,
            choices=STATE_CHOICES,
            maxlength=6,
        ),
        StringField(
            UserDB.full_name.name, "Name",
            required=True,
            maxlength=64,
        ),
        StringField(
            UserDB.username.name, "Username",
            required=False,
            maxlength=65,
        ),
        EnumField(
            UserDB.language_code.name, "Language",
            required=False,
            read_only=True,
            choices=LANGUAGE_CHOICES,
            maxlength=2,
        ),
        DateTimeField(
            UserDB.created_at.name, "Created at",
            read_only=True
        ),
    ]
    form_include_pk = True
    exclude_fields_from_create = ["created_at"]
    searchable_fields = [c.name for c in UserDB.__table__.columns]  # type: ignore

    def can_create(self, request: Request) -> bool:
        return False
