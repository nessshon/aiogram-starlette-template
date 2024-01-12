from dataclasses import dataclass
from pathlib import Path

from environs import Env

BASE_DIR = Path(__file__).resolve().parent


@dataclass
class BotConfig:
    TOKEN: str
    USERNAME: str
    DEV_ID: int
    ADMIN_ID: int


@dataclass
class AppConfig:
    URL: str
    HOST: str
    PORT: int


@dataclass
class AdminConfig:
    BASE_URL: str
    TEMPLATES_DIR: str
    STATICS_DIR: str
    LANGUAGES: list
    TITLE: str


@dataclass
class WebhookConfig:
    SECRET: str
    PATH: str


@dataclass
class RedisConfig:
    HOST: str
    PORT: int
    DB: int

    def dsn(self) -> str:
        """
        Generates a Redis connection DSN (Data Source Name) using the provided host, port, and database.

        :return: The generated DSN.
        """
        return f"redis://{self.HOST}:{self.PORT}/{self.DB}"


@dataclass
class DatabaseConfig:
    USERNAME: str
    PASSWORD: str
    DATABASE: str
    HOST: str
    PORT: int

    def url(self, driver: str = "mysql+aiomysql") -> str:
        """
        Generates a database connection URL using the provided driver, username, password, host, port, and database.

        :param driver: The driver to use for the connection. Defaults to "mysql+aiomysql".
        :return: The generated connection URL.
        """
        return f"{driver}://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"


@dataclass
class Config:
    bot: BotConfig
    app: AppConfig
    admin: AdminConfig
    webhook: WebhookConfig
    redis: RedisConfig
    database: DatabaseConfig


def load_config() -> Config:
    env = Env()
    env.read_env()

    return Config(
        bot=BotConfig(
            TOKEN=env.str("BOT_TOKEN"),
            USERNAME=env.str("BOT_USERNAME"),
            DEV_ID=env.int("BOT_DEV_ID"),
            ADMIN_ID=env.int("BOT_ADMIN_ID"),
        ),
        app=AppConfig(
            URL=env.str("APP_URL"),
            HOST=env.str("APP_HOST"),
            PORT=env.int("APP_PORT"),
        ),
        admin=AdminConfig(
            BASE_URL="/",
            TEMPLATES_DIR="{}/admin/templates".format(BASE_DIR),
            STATICS_DIR="{}/admin/statics".format(BASE_DIR),
            LANGUAGES=["en", "ru"],
            TITLE="Admin Panel",
        ),
        webhook=WebhookConfig(
            SECRET=env.str("WEBHOOK_SECRET"),
            PATH=env.str("WEBHOOK_PATH"),
        ),
        redis=RedisConfig(
            HOST=env.str("REDIS_HOST"),
            PORT=env.int("REDIS_PORT"),
            DB=env.int("REDIS_DB"),
        ),
        database=DatabaseConfig(
            HOST=env.str("MYSQL_HOST"),
            PORT=env.int("MYSQL_PORT"),
            USERNAME=env.str("MYSQL_USER"),
            PASSWORD=env.str("MYSQL_PASSWORD"),
            DATABASE=env.str("MYSQL_DATABASE"),
        ),
    )
