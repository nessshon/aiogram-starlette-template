from aiogram import Dispatcher

from .database import DBSessionMiddleware
from .throttling import ThrottlingMiddleware


def bot_middlewares_register(dp: Dispatcher, **kwargs) -> None:
    """
    Register bot middlewares.
    """
    dp.update.outer_middleware.register(DBSessionMiddleware(kwargs["sessionmaker"]))
    dp.update.outer_middleware.register(ThrottlingMiddleware())


__all__ = [
    "bot_middlewares_register",
]
