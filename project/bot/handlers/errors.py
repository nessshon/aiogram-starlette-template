import asyncio
import logging
import traceback

from aiogram import Router, F, Bot
from aiogram.types import ErrorEvent, BufferedInputFile
from aiogram.utils.markdown import hcode, hbold
from aiogram.exceptions import TelegramBadRequest

from project.config import Config

router = Router()


@router.errors(F.exception.message.contains("query is too old"))
async def query_too_old(_: ErrorEvent) -> None:
    """Handles errors containing 'query is too old'."""


@router.errors()
async def telegram_api_error(event: ErrorEvent, bot: Bot, config: Config) -> None:
    """ Handles Telegram API errors. """
    logging.exception(f'Update: {event.update}\nException: {event.exception}')

    # Prepare data for document
    update_json = event.update.model_dump_json(indent=2, exclude_none=True)
    exc_text, exc_name = str(event.exception), type(event.exception).__name__

    try:
        # Send document with error details
        document_data = traceback.format_exc().encode()
        document_name = f'error_{event.update.update_id}.txt'

        document = BufferedInputFile(document_data, filename=document_name)
        caption = f'{hbold(exc_name)}:\n{hcode(exc_text[:1024 - len(exc_name) - 2])}'
        message = await bot.send_document(config.bot.DEV_ID, document, caption=caption)

        # Send update_json in chunks
        for text in [update_json[i:i + 4096] for i in range(0, len(update_json), 4096)]:
            await asyncio.sleep(.1)
            await message.reply(hcode(text))

    except TelegramBadRequest:
        ...
