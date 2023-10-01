from sqlalchemy import *
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from ._base import Base


class User(Base):
    """
    Model representing User table.

    Inherits from the Base class.
    """
    __tablename__ = "users"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    state = Column(
        VARCHAR(length=6),
        nullable=False,
        default="member",
    )
    user_id = Column(
        BigInteger,
        unique=True,
        nullable=False,
    )
    first_name = Column(
        VARCHAR(length=128),
        nullable=False,
    )
    username = Column(
        VARCHAR(length=64),
        nullable=True,
    )
    created_at = Column(
        DateTime,
        default=func.now(),
        nullable=False,
    )

    async def __admin_repr__(self, _) -> str:
        """
        Get the string representation of a user for admin panel.
        """
        return f"#{self.id} {self.username} [{self.user_id}]"

    async def __admin_select2_repr__(self, _) -> str:
        """
        Get the HTML representation of a user for admin panel.
        """
        return f"<span>#{self.id} {self.username} [{self.user_id}]</span>"

    @staticmethod
    async def get(session: AsyncSession, **kwargs) -> 'User':
        """
        Get a user from the database based on the specified filters.

        :param session: The asynchronous SQLAlchemy session.
        :param kwargs: The filters for selecting the user.
        :return: The user object or None if not found.
        """
        filters = [*[getattr(User, key) == v for key, v in kwargs.items()]]
        query = await session.execute(select(User).where(*filters))
        return query.scalar()

    @staticmethod
    async def get_or_create(session: AsyncSession, user_id: int, **kwargs):
        """
        Get a user from the database based on the specified filters, or create a new user if not found.

        :param session: The asynchronous SQLAlchemy session.
        :param user_id: The ID of the user.
        :param kwargs: Additional parameters for creating a new user.
        :return: The user object.
        """
        filters = [User.user_id == user_id]
        result = await session.execute(select(User).filter(*filters))

        try:
            user = result.scalar_one()
            for key, value in kwargs.items():
                setattr(user, key, value)
        except NoResultFound:
            user = User(user_id=user_id, **kwargs)

        await session.flush()
        return user

    @staticmethod
    async def update(session, user_id: int, **kwargs) -> None:
        """
        Update a user in the database based on the specified filters.

        :param session: The asynchronous SQLAlchemy session.
        :param user_id: The ID of the user to be updated.
        :param kwargs: The attributes to be updated.
        """
        filters = [User.user_id == user_id]
        await session.execute(update(User).filter(*filters).values(**kwargs))
        await session.commit()

    @staticmethod
    async def is_exist(session: AsyncSession, **kwargs) -> bool:
        """
        Check if a user with the given ID exists in the database.

        :param session: The asynchronous SQLAlchemy session.
        :param kwargs:  The filters for querying the existence of a User object.
        :return: True if the user exists, False otherwise.
        """
        filters = [*[getattr(User, key) == v for key, v in kwargs.items()]]
        query = await session.execute(select(User).filter(*filters))
        return bool(query.scalar())
