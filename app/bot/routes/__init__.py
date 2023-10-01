from aiogram import Dispatcher

from . import private

from . import error
from . import inline


def bot_routers_include(dp: Dispatcher) -> None:
    """
    Include bot routers.
    """
    dp.include_routers(
        *[
            error.router,
            private.command.router,
            private.callback.router,
            private.message.router,
            private.my_chat_member.router,
            inline.router,
        ]
    )


__all__ = [
    "bot_routers_include",
]
