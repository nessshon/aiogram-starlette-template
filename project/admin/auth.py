# https://github.com/jowilf/starlette-admin/tree/main/examples/auth

import asyncio
import hashlib
import hmac

from dataclasses import dataclass, asdict
from typing import Optional

from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from starlette_admin import BaseAdmin
from starlette_admin.auth import AdminUser as BaseAdminUser
from starlette_admin.auth import AuthProvider as BaseAuthProvider
from starlette_admin.auth import AuthMiddleware as BaseAuthMiddleware
from starlette_admin.exceptions import LoginFailed

from project.config import Config
from project.db.models import AdminDB
from project.admin.views import AdminRoles


def is_data_authentic(data: dict, bot_token: str) -> bool:
    """
    Check if the data received from Telegram OAuth is authentic and not tampered with.

    :param data: The data received from Telegram OAuth.
    :param bot_token: The bot token used to calculate the HMAC hash.
    :return: True if the data is authentic, False otherwise.
    """
    check_hash = data.pop('hash')
    check_list = ['{}={}'.format(k, v) for k, v in data.items()]
    check_string = '\n'.join(sorted(check_list))

    secret_key = hashlib.sha256(str.encode(bot_token)).digest()
    hmac_hash = hmac.new(secret_key, str.encode(check_string), hashlib.sha256, ).hexdigest()

    return hmac_hash == check_hash


@dataclass
class OAuthData:
    id: Optional[int] = None
    auth_date: Optional[int] = None
    first_name: Optional[str] = None
    hash: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None

    def to_dict(self) -> dict:
        """
        Convert the data to a dictionary.
        """
        return asdict(self)


@dataclass
class AdminUser(BaseAdminUser):
    id: Optional[int] = None
    roles: Optional[list] = None
    first_name: Optional[str] = None
    auth_date: Optional[int] = None

    def to_dict(self) -> dict:
        """
        Convert the data to a dictionary.
        """
        return asdict(self)


class AuthProvider(BaseAuthProvider):
    """
    Custom authentication provider for handling login and logout.

    Inherits from the base AuthProvider class.
    """

    async def render_login(self, request: Request, admin: 'BaseAdmin') -> Response:
        """
        Render the login page for the admin.

        :param request: The request object.
        :param admin: The BaseAdmin object.
        :return: The response containing the rendered login page.
        """
        if request.method == "GET":
            config: Config = request.state.config
            return admin.templates.TemplateResponse(
                "login.html",
                {
                    "request": request,
                    "bot_username": config.bot.USERNAME,
                    "redirect_url": config.app.URL + config.admin.BASE_URL,
                },
            )

        return await self.login(
            "username",  # type: ignore
            "password",  # type: ignore
            True,
            request,
            RedirectResponse(
                request.url_for(admin.route_name + ":index"),
                status_code=HTTP_303_SEE_OTHER,
            ),
        )

    async def login(
            self,
            username: str,
            password: str,
            remember_me: bool,
            request: Request,
            response: Response,
    ) -> Response:
        """
        Handle the login process.

        :param username: Not used.
        :param password: Not used.
        :param remember_me: Not used.
        :param request: The request object.
        :param response: The response object.
        :return: The response after successful login or raising a LoginFailed exception.
        """
        data = await request.json()
        auth_data = OAuthData(**data)
        config: Config = request.state.config

        if auth_data.id in [config.bot.ADMIN_ID, config.bot.DEV_ID]:
            roles = AdminRoles.all()
        else:
            admin = await AdminDB.get_by_key(request.state.sessionmaker, AdminDB.user_id, auth_data.id)
            roles = admin.roles if admin else None

        if roles and is_data_authentic(auth_data.to_dict(), config.bot.TOKEN):
            admin_user = AdminUser(
                id=auth_data.id,
                roles=roles,
                username=auth_data.username,
                photo_url=auth_data.photo_url,
                first_name=auth_data.first_name,
                auth_date=auth_data.auth_date
            )
            request.session.update(admin_user.to_dict())
            return response

        raise LoginFailed(msg='Login failed.')

    async def is_authenticated(self, request) -> bool:
        """
        Check if the user is authenticated.

        :param request: The request object.
        :return: True if the user is authenticated, False otherwise.
        """
        config: Config = request.state.config
        admin_id = request.session.get("id", None)
        if (
                admin_id in [config.bot.ADMIN_ID, config.bot.DEV_ID] or
                await AdminDB.get_by_key(request.state.sessionmaker, AdminDB.user_id, admin_id)
        ):
            request.state.user = request.session
            return True
        return False

    def get_admin_user(self, request) -> AdminUser:
        """
        Get the admin user.

        :param request: The request object.
        :return: The admin user as a MyAdminUser object.
        """
        config: Config = request.state.config
        admin_id = request.session.get("id")

        if admin_id not in [config.bot.ADMIN_ID, config.bot.DEV_ID]:
            async def get_admin():
                admin = await AdminDB.get(request.state.sessionmaker, admin_id)
                request.state.user["roles"] = admin.roles

            asyncio.create_task(get_admin())

        return AdminUser(**request.state.user)

    async def logout(self, request: Request, response: Response) -> Response:
        """
        Handle the logout process.

        :param request: The request object.
        :param response: The response object.
        :return: The response after successful logout.
        """
        request.session.clear()
        return response


class AuthMiddleware(BaseAuthMiddleware):
    """
    Custom authentication middleware for adding authentication to routes.

    Inherits from the base AuthMiddleware class.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """
        Perform the authentication check and dispatch the request.

        :param request: The request object.
        :param call_next: The next request-response call.
        :return: The response from the next call or a redirect response if authentication fails.
        """
        if request.scope["path"] not in self.allow_paths and not (
                await self.provider.is_authenticated(request)
        ):
            return RedirectResponse(
                "{url}".format(
                    url=request.url_for(request.app.state.ROUTE_NAME + ":login"),
                ),
                status_code=HTTP_303_SEE_OTHER,
            )
        return await call_next(request)
