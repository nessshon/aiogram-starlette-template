from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

router = Router()
router.message.filter(F.chat.type == "private")


@router.message(Command("start"))
async def handler(message: Message) -> None:
    """
    Example start command.
    """
    await message.answer("Hello from Bot!")
