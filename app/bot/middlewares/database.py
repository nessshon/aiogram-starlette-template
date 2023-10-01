from typing import Callable, Awaitable, Dict, Any, Optional

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.types import User as TelegramUser
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.db.models import User


class DBSessionMiddleware(BaseMiddleware):
    """
    Middleware for handling database sessions.
    """

    def __init__(self, session: async_sessionmaker):
        """
        Initialize the DBSessionMiddleware.

        :param session: The async sessionmaker object for creating database sessions.
        """
        super().__init__()
        self.session = session

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        """
        Call the middleware.

        :param handler: The handler function.
        :param event: The Telegram event.
        :param data: Additional data.
        """
        session: AsyncSession
        async with self.session() as session:
            user: Optional[TelegramUser] = data.get("event_from_user", None)

            if user is not None: user = await User.get_or_create(  # noqa:E701
                session,
                user_id=user.id,
                first_name=user.first_name,
                username=user.username
            )
            data["user"] = user
            data["session"] = session
            return await handler(event, data)
