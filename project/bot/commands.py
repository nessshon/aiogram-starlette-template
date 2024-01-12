from aiogram import Bot
from aiogram.types import (
    BotCommand,
    BotCommandScopeAllPrivateChats,
)


async def bot_commands_setup(bot: Bot) -> None:
    """
    Setup bot commands.

    :param bot: The Bot object.
    """
    commands = [
        BotCommand(command="start", description="Restart bot"),
    ]

    # Set commands for all private chats in English language
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeAllPrivateChats(),
    )


async def bot_commands_delete(bot: Bot) -> None:
    """
    Delete bot commands.

    :param bot: The Bot object.
    """
    # Delete commands for all private chats in any language
    await bot.delete_my_commands(
        scope=BotCommandScopeAllPrivateChats(),
    )
