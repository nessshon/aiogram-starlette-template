from typing import Awaitable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class BotMiddleware(BaseHTTPMiddleware):
    """
    Middleware for adding a bot instance to the request state.

    Inherits from the base BaseHTTPMiddleware class.
    """

    def __init__(self, bot, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bot = bot

    async def dispatch(self, request, call_next) -> Response:
        """
        Dispatch the request and add the bot instance to the request state.

        :param request: The request object.
        :param call_next: The next request-response call.
        :return: The response from the next call.
        """
        request.state.bot = self.bot
        response = await call_next(request)
        return response
