from __future__ import annotations

from aiogram.enums import ChatMemberStatus
from sqlalchemy import *

from ._abc import AbstractModel


class UserDB(AbstractModel):
    """
    Model representing User table.
    """
    id = Column(
        BigInteger,
        primary_key=True,
        nullable=False,
    )
    state = Column(
        VARCHAR(length=6),
        nullable=False,
        default=ChatMemberStatus.MEMBER,
    )
    full_name = Column(
        VARCHAR(length=128),
        nullable=False,
    )
    username = Column(
        VARCHAR(length=65),
        nullable=True,
    )
    language_code = Column(
        VARCHAR(length=2),
        nullable=True,
    )
    created_at = Column(
        DateTime,
        default=func.now(),
        nullable=False,
    )

    __tablename__ = "users"

    __admin_icon__ = "fas fa-user"
    __admin_label__ = "User"
    __admin_name__ = "Users"
    __admin_identity__ = "user"

    async def __admin_repr__(self, _) -> str:
        """
        Get the string representation of a user for admin panel.
        """
        return f"{self.username or self.full_name} [{self.id}]"

    async def __admin_select2_repr__(self, _) -> str:
        """
        Get the HTML representation of a user for admin panel.
        """
        return f"<span>{self.username or self.full_name} [{self.id}]</span>"
