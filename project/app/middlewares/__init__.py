from fastapi import FastAPI

from .bot import BotMiddleware
from .config import ConfigMiddleware
from .database import DBSessionMiddleware


def app_middlewares_register(app: FastAPI, **kwargs) -> None:
    """
    Register app middlewares.
    """
    app.add_middleware(DBSessionMiddleware, sessionmaker=kwargs["sessionmaker"])  # type: ignore
    app.add_middleware(ConfigMiddleware, config=kwargs["config"])  # type: ignore
    app.add_middleware(BotMiddleware, bot=kwargs["bot"])  # type: ignore


__all__ = [
    "app_middlewares_register",
]
