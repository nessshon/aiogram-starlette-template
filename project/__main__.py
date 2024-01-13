from contextlib import asynccontextmanager

import uvicorn
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Update
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from starlette_admin import I18nConfig

from .admin.admin import Admin
from .admin.auth import AuthMiddleware, AuthProvider
from .admin.views import admin_views_add
from .app.routes import app_routers_include
from .app.middlewares import app_middlewares_register
from .bot.commands import bot_commands_setup, bot_commands_delete
from .bot.handlers import bot_routers_include
from .bot.middlewares import bot_middlewares_register
from .config import load_config
from .db.models import Base
from .logger import setup_logger


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Async context manager for startup and shutdown lifecycle events.

    - Creates database tables.
    - Sets up bot commands and webhook.

    Yields control during application's lifespan and performs cleanup on exit.

    - Disposes all database connections.
    - Deletes bot webhook and commands.
    - Closes aiohttp session.
    """
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    await bot_commands_setup(bot)
    await bot.set_webhook(url=webhook_url, allowed_updates=dp.resolve_used_update_types())

    try:
        yield
    finally:
        # Cleanup actions
        await engine.dispose()
        await bot_commands_delete(bot)
        await bot.delete_webhook()
        await bot.session.close()


async def bot_webhook(update: dict) -> Response:
    """
    Bot webhook endpoint. Receives updates and feeds them to the bot dispatcher.
    :param update: The update received from the bot webhook.
    """
    await dp.feed_update(bot=bot, update=Update(**update))
    return Response()


# Create FastAPI app and config
app = FastAPI(lifespan=lifespan)
config = load_config()

# Set webhook path and URL
webhook_path = config.webhook.PATH + config.bot.TOKEN
webhook_url = config.app.URL + webhook_path

# Create async engine and async_sessionmaker
engine = create_async_engine(
    url=config.database.url(),
    pool_pre_ping=True,
)
sessionmaker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Create bot and dispatcher instances
bot = Bot(
    token=config.bot.TOKEN,
    parse_mode=ParseMode.HTML,
)
storage = RedisStorage.from_url(
    url=config.redis.dsn(),
)
dp = Dispatcher(
    storage=storage,
    config=config,
)

# Create admin instance
admin = Admin(
    engine=engine,
    title=config.admin.TITLE,
    base_url=config.admin.BASE_URL,
    statics_dir=config.admin.STATICS_DIR,
    templates_dir=config.admin.TEMPLATES_DIR,
    i18n_config=I18nConfig(
        default_locale=config.admin.LANGUAGES[0],
    ),
    auth_provider=AuthProvider(),
    middlewares=[
        Middleware(SessionMiddleware, secret_key=config.webhook.SECRET),  # type: ignore
        Middleware(AuthMiddleware, provider=AuthProvider()),  # type: ignore
    ],
)

# Mount static files directory
app.mount("/static", name="statics", app=StaticFiles(directory=config.admin.STATICS_DIR))
# Register app middlewares
app_middlewares_register(app, bot=bot, config=config, sessionmaker=sessionmaker)
# Include app routes
app_routers_include(app)
# Register bot webhook
app.add_api_route(webhook_path, endpoint=bot_webhook, methods=["POST"])

# Register bot middlewares
bot_middlewares_register(dp, config=config, redis=storage.redis, sessionmaker=sessionmaker)
# Include bot routers
bot_routers_include(dp)

# Initialize admin routes
admin.init_routes()
# Mount admin panel
admin.mount_to(app)
# Add admin views
admin_views_add(admin)

if __name__ == '__main__':
    # Set up logger
    setup_logger()
    # Run app with uvicorn
    uvicorn.run(
        app,
        host=config.app.HOST,
        port=config.app.PORT,
        forwarded_allow_ips="*",
    )
