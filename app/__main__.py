import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

import uvicorn
from aiogram.enums import ParseMode
from aiogram.types import Update
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from starlette_admin import I18nConfig
from starlette_admin.contrib.sqla import Admin

from .admin.auth import MyAuthMiddleware, MyAuthProvider
from .admin.views import admin_views_add
from .app.routes import app_routers_include
from .app.middlewares import app_middlewares_register
from .bot import commands
from .bot.routes import bot_routers_include
from .bot.middlewares import bot_middlewares_register
from .config import load_config
from .db.database import Database

config = load_config()
webhook_path = config.webhook.PATH + config.bot.TOKEN
webhook_url = config.webhook.DOMAIN + webhook_path

app = FastAPI(debug=config.app.DEBUG)
db = Database(config=config.database)
bot = Bot(
    token=config.bot.TOKEN,
    parse_mode=ParseMode.HTML,
)
dp = Dispatcher(
    storage=RedisStorage.from_url(config.redis.dsn()),
    config=config,
)
admin = Admin(
    engine=db.engine,
    debug=config.app.DEBUG,
    title=config.admin.TITLE,
    base_url=config.admin.BASE_URL,
    statics_dir=config.admin.STATICS_DIR,
    templates_dir=config.admin.TEMPLATES_DIR,
    i18n_config=I18nConfig(
        default_locale=config.admin.LANGUAGES[0],
        language_switcher=config.admin.LANGUAGES,
    ),
    auth_provider=MyAuthProvider(),
    middlewares=[
        Middleware(SessionMiddleware, secret_key=config.webhook.SECRET),
        Middleware(MyAuthMiddleware, provider=MyAuthProvider()),
    ],
)


async def bot_webhook(update: dict) -> Response:
    """
    Bot webhook endpoint. Receives updates and feeds them to the bot dispatcher.

    :param update: The update received from the bot webhook.
    """
    await dp.feed_update(bot=bot, update=Update(**update))

    return Response()


@app.on_event("startup")
async def on_startup() -> None:
    """
    Startup event handler. This runs when the app starts.
    """
    await db.init()
    await commands.setup(bot)
    await bot.send_message(chat_id=config.bot.DEV_ID, text="#BotStarted")
    await bot.set_webhook(url=webhook_url, allowed_updates=dp.resolve_used_update_types())


@app.on_event("shutdown")
async def on_shutdown() -> None:
    """
    Shutdown event handler. This runs when the app shuts down.
    """
    await db.close()
    await commands.delete(bot)
    await bot.send_message(chat_id=config.bot.DEV_ID, text="#BotStopped")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()


# Mount static files directory
app.mount(path="/static", name="statics", app=StaticFiles(directory=config.admin.STATICS_DIR))
# Register app middlewares
app_middlewares_register(app=app, bot=bot, config=config, session=db.session)
# Include app routes
app_routers_include(app=app)

# Register bot webhook
app.add_api_route(webhook_path, endpoint=bot_webhook, methods=["POST"])
# Register bot middlewares
bot_middlewares_register(dp=dp, config=config, session=db.session)
# Include bot routers
bot_routers_include(dp=dp)

# Initialize admin routes
admin.init_routes()
# Mount admin panel
admin.mount_to(app)
# Add admin views
admin_views_add(admin)

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # noqa
        handlers=[
            TimedRotatingFileHandler(
                filename=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
                when="midnight",
                interval=1,
                backupCount=1,
            ),
            logging.StreamHandler(),
        ]
    )
    # Set logging level for aiogram to CRITICAL
    aiogram_logger = logging.getLogger("aiogram.event")
    aiogram_logger.setLevel(logging.CRITICAL)
    # Run app with uvicorn
    uvicorn.run(app, host=config.app.HOST, port=config.app.PORT)
