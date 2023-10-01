import logging
import traceback

from aiogram import Router, Bot
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent, BufferedInputFile
from aiogram.utils.markdown import hcode, hbold
from aiogram.exceptions import TelegramBadRequest

from app.config import Config

router = Router()


@router.errors(ExceptionTypeFilter(Exception))
async def telegram_api_error(event: ErrorEvent, bot: Bot, config: Config) -> bool:
    logging.exception(f'Update: {event.update}\nException: {event.exception}')

    try:
        document_message = await bot.send_document(
            chat_id=config.bot.DEV_ID,
            document=BufferedInputFile(
                traceback.format_exc().encode(),
                filename=f'error_{event.update.update_id}.txt',
            ),
            caption=f'{hbold(type(event.exception).__name__)}: {str(event.exception)[:1021]}...',
        )

        update_json = event.update.model_dump_json(indent=2, exclude_none=True)
        chunks = [update_json[i:i + 4096] for i in range(0, len(update_json), 4096)]
        [await document_message.reply(text=hcode(chunk)) for chunk in chunks]

    except TelegramBadRequest:
        pass

    return True
