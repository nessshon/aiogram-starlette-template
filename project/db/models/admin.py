from sqlalchemy import *
from sqlalchemy.orm import relationship, Mapped, mapped_column

from ._abc import AbstractModel


class AdminDB(AbstractModel):
    """
    Model representing Admin table.
    """
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    user_id = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    roles = mapped_column(
        JSON,
        nullable=False,
        default=[],
    )
    created_at = mapped_column(
        DateTime,
        default=func.now(),
    )
    user: Mapped["UserDB"] = relationship("UserDB", backref="admin_users")

    __tablename__ = "admins"
    __admin_icon__ = "fas fa-user-tie"
    __admin_label__ = "Admin"
    __admin_name__ = "Admins"
    __admin_identity__ = "admin"
