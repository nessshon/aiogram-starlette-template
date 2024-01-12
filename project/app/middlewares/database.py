from sqlalchemy.ext.asyncio import async_sessionmaker
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class DBSessionMiddleware(BaseHTTPMiddleware):
    """
    Middleware for managing the database session.
    """

    def __init__(self, sessionmaker: async_sessionmaker, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.sessionmaker = sessionmaker

    async def dispatch(self, request, call_next) -> Response:
        """
        Dispatch the request and manage the database session.

        :param request: The request object.
        :param call_next: The next request-response call.
        :return: The response from the next call.
        """
        request.state.sessionmaker = self.sessionmaker
        response = await call_next(request)
        return response
