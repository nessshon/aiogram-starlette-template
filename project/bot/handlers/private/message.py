from aiogram import Router, F
from aiogram.types import Message

router = Router()
router.message.filter(F.chat.type == "private")


@router.message()
async def example_error_handler(_: Message) -> None:
    """
    Example error handler.
    """
    raise RuntimeError("Example error")
