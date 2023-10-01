from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class ConfigMiddleware(BaseMiddleware):
    """
    Middleware for passing config data.
    """
    def __init__(self, config) -> None:
        """
        Initialize the ConfigMiddleware.

        :param config: The config data to be passed.
        """
        self.config = config

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
        data["config"] = self.config
        return await handler(event, data)
