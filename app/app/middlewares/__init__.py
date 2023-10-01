from fastapi import FastAPI

from .bot import BotMiddleware
from .config import ConfigMiddleware
from .database import DBSessionMiddleware


def app_middlewares_register(app: FastAPI, **kwargs) -> None:
    """
    Register app middlewares.
    """
    app.add_middleware(DBSessionMiddleware, session=kwargs["session"])
    app.add_middleware(ConfigMiddleware, config=kwargs["config"])
    app.add_middleware(BotMiddleware, bot=kwargs["bot"])


__all__ = [
    "app_middlewares_register",
]
