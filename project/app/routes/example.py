from aiogram import Bot
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response

from project.config import Config

router = APIRouter()


@router.get("/example")
@router.post("/example")
async def handler(request: Request) -> Response:
    """
    Example separate api route.
    """
    bot: Bot = request.state.bot
    config: Config = request.state.config
    await bot.send_message(chat_id=config.bot.DEV_ID, text="Hello from FastAPI!")

    content = {"ok": f"Message sent to {config.bot.DEV_ID}!"}.__str__()
    return Response(content, media_type="application/json")
