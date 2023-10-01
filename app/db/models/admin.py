from sqlalchemy import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from ._base import Base


class Admin(Base):
    """
    Model representing Admin table.

    Inherits from the Base class.
    """
    __tablename__ = "admins"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    user_id = Column(
        BigInteger,
        ForeignKey(
            "users.user_id",
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
    user = relationship("User", backref="users")

    @staticmethod
    async def get(session: AsyncSession, **kwargs) -> 'Admin':
        """
        Get the Admin object from the database based on the specified filters.

        :param session: The asynchronous SQLAlchemy session.
        :param kwargs: The filters for selecting the Admin object.
        :return: The Admin object or None if not found.
        """
        filters = [*[getattr(Admin, key) == v for key, v in kwargs.items()]]
        query = await session.execute(select(Admin).where(*filters))
        return query.scalar()

    @staticmethod
    async def is_exists(session: AsyncSession, **kwargs) -> bool:
        """
        Check if an Admin object exists in the database based on the specified filters.

        :param session: The asynchronous SQLAlchemy session.
        :param kwargs: The filters for querying the existence of an Admin object.
        :return: True if an Admin object exists, False otherwise.
        """
        filters = [*[getattr(Admin, key) == v for key, v in kwargs.items()]]
        query = await session.execute(select(Admin).filter(*filters))
        return bool(query.scalar())
