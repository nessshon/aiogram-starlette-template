from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from . import models
from ..config import DatabaseConfig


class Database:
    """
    Database manager for handling database connections and operations.
    """

    def __init__(self, config: DatabaseConfig) -> None:
        """
        Initialize the Database manager.

        :param config: The database configuration object.
        """
        self.engine = create_async_engine(
            url=config.url(),
            pool_pre_ping=True,
        )
        self.session = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def init(self) -> 'Database':
        """
        Initialize the database.

        :return: The initialized Database instance.
        """
        async with self.engine.begin() as connection:
            await connection.run_sync(models.Base.metadata.create_all)
        return self

    async def close(self) -> None:
        """
        Close the database connection.
        """
        await self.engine.dispose()
