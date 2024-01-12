from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from project.config import Config


class ConfigMiddleware(BaseHTTPMiddleware):
    """
    Middleware for handling the application configuration.
    """

    def __init__(self, config: Config, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.config = config

    async def dispatch(self, request, call_next) -> Response:
        """
        Dispatch the request and set the configuration in the request state.

        :param request: The request object.
        :param call_next: The next request-response call.
        :return: The response from the next call.
        """
        request.state.config = self.config
        response = await call_next(request)
        return response
