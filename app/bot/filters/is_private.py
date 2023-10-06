from aiogram.enums import ChatType
from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject, Chat


class IsPrivate(BaseFilter):
    """
    Filter for checking if a message is in a private chat.
    """

    async def __call__(self, event: TelegramObject, event_chat: Chat) -> bool:
        """
        Call the filter.

        :param event: The event object (e.g., Message) to check.
        :param event_chat: The chat object associated with the event.
        :return: True if the message is in a private chat, False otherwise.
        """
        return event_chat.type == ChatType.PRIVATE
