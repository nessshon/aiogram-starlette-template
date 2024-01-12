from sqlalchemy import *
from sqlalchemy.orm import relationship

from ._abc import AbstractModel


class AdminDB(AbstractModel):
    """
    Model representing Admin table.
    """
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    user_id = Column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    roles = Column(
        JSON,
        nullable=False,
        default=[],
    )
    created_at = Column(
        DateTime,
        default=func.now(),
    )
    user = relationship("UserDB", backref="admin_users")

    __tablename__ = "admins"

    __admin_icon__ = "fas fa-user-tie"
    __admin_label__ = "Admin"
    __admin_name__ = "Admins"
    __admin_identity__ = "admin"
