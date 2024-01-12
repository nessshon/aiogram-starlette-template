from __future__ import annotations

import typing as t

from sqlalchemy import *
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import InstrumentedAttribute

from ._base import Base

T = t.TypeVar("T", bound="AbstractModel")


class AbstractModel(Base):
    """Base class for all models."""

    __abstract__ = True
    __allow_unmapped__ = True

    def to_dict(self) -> t.Dict:
        """
        Convert the data to a dictionary.
        """
        return {f"{self.__tablename__}_{col.name}": getattr(self, col.name) for col in
                t.cast(t.List[Column], self.__table__.columns)}

    @staticmethod
    def _get_column(
            model: t.Type[T],
            col: InstrumentedAttribute[t.Any],
    ) -> str:
        """Get the name of a column in a model."""
        name = col.name
        if name not in model.__table__.columns:
            raise ValueError(f"Column {name} not found in {model.__name__}")
        return name

    @classmethod
    def _get_primary_key(cls) -> str:
        """Return the primary key of the model."""
        return cls.__table__.primary_key.columns.values()[0].name

    @classmethod
    async def create(
            cls: t.Type[T],
            sessionmaker: async_sessionmaker,
            **kwargs,
    ) -> T:
        """Create a new record in the database."""
        async with sessionmaker() as async_session:
            instance = cls(**kwargs)
            async_session.add(instance)
            await async_session.commit()
            await async_session.refresh(instance)
            return instance

    @classmethod
    async def get(
            cls: t.Type[T],
            sessionmaker: async_sessionmaker,
            primary_key: int,
    ) -> T:
        """Get a record from the database by its primary key."""
        async with sessionmaker() as async_session:
            return await async_session.get(cls, primary_key)

    @classmethod
    async def get_by_key(
            cls: t.Type[T],
            sessionmaker: async_sessionmaker,
            key: InstrumentedAttribute[t.Any],
            value: t.Any,
    ) -> T | None:
        """Get a record by a key."""
        async with sessionmaker() as async_session:
            statement = select(cls).filter_by(**{cls._get_column(cls, key): value})
            result = await async_session.execute(statement)
            return result.scalars().first()

    @classmethod
    async def update(
            cls: t.Type[T],
            sessionmaker: async_sessionmaker,
            primary_key: int,
            **kwargs,
    ) -> T:
        """Update a record in the database by its primary key."""
        async with sessionmaker() as async_session:
            instance = await cls.get(sessionmaker, primary_key)
            if instance:
                for attr, value in kwargs.items():
                    setattr(instance, attr, value)
                async_session.add(instance)
                await async_session.commit()
            return instance

    @classmethod
    async def update_by_key(
            cls: t.Type[T],
            sessionmaker: async_sessionmaker,
            key: InstrumentedAttribute[t.Any],
            value: t.Any,
            **kwargs,
    ) -> T:
        """Update a record in the database by a key."""
        async with sessionmaker() as async_session:
            instance = await cls.get_by_key(sessionmaker, key, value)
            if instance:
                for attr, value in kwargs.items():
                    setattr(instance, attr, value)
                async_session.add(instance)
                await async_session.commit()
            return instance

    @classmethod
    async def delete(
            cls: t.Type[T],
            sessionmaker: async_sessionmaker,
            primary_key: int,
    ) -> None:
        """Delete a record from the database by its primary key."""
        async with sessionmaker() as async_session:
            instance = await cls.get(sessionmaker, primary_key)
            if instance:
                await async_session.delete(instance)
                await async_session.commit()

    @classmethod
    async def delete_by_key(
            cls: t.Type[T],
            sessionmaker: async_sessionmaker,
            key: InstrumentedAttribute[t.Any],
            value: t.Any,
    ) -> None:
        """Delete a record from the database by a key."""
        async with sessionmaker() as async_session:
            instance = await cls.get_by_key(sessionmaker, key, value)
            if instance:
                await async_session.delete(instance)
                await async_session.commit()

    @classmethod
    async def create_or_update(
            cls: t.Type[T],
            sessionmaker: async_sessionmaker,
            **kwargs,
    ) -> T:
        """Get and update a record from the database by its primary key."""
        primary_key = kwargs.get(cls._get_primary_key())
        instance = await cls.get(sessionmaker, primary_key)
        if instance:
            await cls.update(sessionmaker, primary_key, **kwargs)
            return instance
        return await cls.create(sessionmaker, **kwargs)

    @classmethod
    async def exists(
            cls: t.Type[T],
            sessionmaker: async_sessionmaker,
            primary_key: int,
    ) -> bool:
        """Check if a record exists in the database by its primary key."""
        async with sessionmaker() as async_session:
            return await async_session.get(cls, primary_key) is not None

    @classmethod
    async def exists_by_filter(
            cls: t.Type[T],
            sessionmaker: async_sessionmaker,
            **kwargs,
    ) -> bool:
        """Check if a record exists in the database by a filter."""
        async with sessionmaker() as async_session:
            statement = select(cls).filter_by(**kwargs).order_by(cls.id.asc())
            result = await async_session.execute(statement)
            return bool(result.scalar())

    @classmethod
    async def paginate(
            cls: t.Type[T],
            sessionmaker: async_sessionmaker,
            page_number: int,
            page_size: int = 10,
    ) -> t.Sequence[T]:
        """Get paginated records from the database."""
        async with sessionmaker() as async_session:
            statement = select(cls).limit(page_size).offset((page_number - 1) * page_size)
            result = await async_session.execute(statement)
            return result.scalars().all()

    @classmethod
    async def paginate_by_filter(
            cls: t.Type[T],
            sessionmaker: async_sessionmaker,
            page_number: int,
            page_size: int = 10,
            **kwargs,
    ) -> t.Sequence[T]:
        """Get paginated records from the database by a filter."""
        async with sessionmaker() as async_session:
            statement = (
                select(cls)
                .filter_by(**kwargs)
                .limit(page_size).offset((page_number - 1) * page_size)
            )
            result = await async_session.execute(statement)
            return result.scalars().all()

    @classmethod
    async def total_pages(
            cls: t.Type[T],
            sessionmaker: async_sessionmaker,
            page_size: int = 10,
    ) -> int:
        async with sessionmaker() as async_session:
            statement = select(func.count(cls.__table__.primary_key.columns[0]))
            query = await async_session.execute(statement)
            return (query.scalar() + page_size - 1) // page_size

    @classmethod
    async def total_pages_by_filter(
            cls: t.Type[T],
            sessionmaker: async_sessionmaker,
            page_size: int = 10,
            **kwargs,
    ) -> int:
        async with sessionmaker() as async_session:
            statement = (
                select(func.count(cls.__table__.primary_key.columns[0]))
                .filter_by(**kwargs)
            )
            query = await async_session.execute(statement)
            return (query.scalar() + page_size - 1) // page_size

    @classmethod
    async def all(
            cls: t.Type[T],
            sessionmaker: async_sessionmaker,
    ) -> t.Sequence[T]:
        """Get all records from the database."""
        async with sessionmaker() as async_session:
            statement = select(cls)
            result = await async_session.execute(statement)
            return result.scalars().all()

    @classmethod
    async def all_by_filter(
            cls: t.Type[T],
            sessionmaker: async_sessionmaker,
            **kwargs,
    ) -> t.Sequence[T]:
        """Get all records from the database by a filter."""
        async with sessionmaker() as async_session:
            statement = select(cls).filter_by(**kwargs)
            result = await async_session.execute(statement)
            return result.scalars().all()
