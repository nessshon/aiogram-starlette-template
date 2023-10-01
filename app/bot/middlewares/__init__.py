from aiogram import Dispatcher

from .config import ConfigMiddleware
from .database import DBSessionMiddleware
from .throttling import ThrottlingMiddleware


def bot_middlewares_register(dp: Dispatcher, **kwargs) -> None:
    """
    Register bot middlewares.
    """
    dp.update.outer_middleware.register(DBSessionMiddleware(kwargs["session"]))
    dp.update.outer_middleware.register(ConfigMiddleware(kwargs["config"]))
    dp.update.outer_middleware.register(ThrottlingMiddleware())


__all__ = [
    "bot_middlewares_register",
]
