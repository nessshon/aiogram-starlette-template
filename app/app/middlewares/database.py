from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class DBSessionMiddleware(BaseHTTPMiddleware):
    """
    Middleware for managing the database session.

    Inherits from the base BaseHTTPMiddleware class.
    """

    def __init__(self, session, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.session = session

    async def dispatch(self, request, call_next) -> Response:
        """
        Dispatch the request and manage the database session.

        This method assigns the session to the request state and ensures it is closed correctly.

        :param request: The request object.
        :param call_next: The next request-response call.
        :return: The response from the next call.
        """
        async with self.session() as session:
            request.state.db_session = session
            response = await call_next(request)
            return response
