from __future__ import annotations

from datetime import datetime

from aiogram.enums import ChatMemberStatus
from sqlalchemy import *
from sqlalchemy.orm import mapped_column, Mapped

from ._abc import AbstractModel


class UserDB(AbstractModel):
    """
    Model representing User table.
    """
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        nullable=False,
    )
    state: Mapped[str] = mapped_column(
        VARCHAR(length=6),
        nullable=False,
        default=ChatMemberStatus.MEMBER,
    )
    full_name: Mapped[str] = mapped_column(
        VARCHAR(length=128),
        nullable=False,
    )
    username: Mapped[str] = mapped_column(
        VARCHAR(length=65),
        nullable=True,
    )
    language_code: Mapped[str] = mapped_column(
        VARCHAR(length=2),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
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
