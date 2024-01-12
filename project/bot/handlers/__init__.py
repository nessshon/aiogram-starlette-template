from aiogram import Dispatcher

from . import private
from . import errors


def bot_routers_include(dp: Dispatcher) -> None:
    """
    Include bot routers.
    """
    dp.include_routers(
        *[
            errors.router,
            private.command.router,

            private.callback_query.router,
            private.inline_query.router,
            private.message.router,

            private.my_chat_member.router,
        ]
    )


__all__ = [
    "bot_routers_include",
]
