from typing import AsyncGenerator, Callable
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def async_session(
    url: str | None,
) -> Callable[..., AsyncGenerator[AsyncSession, None]]:

    if not url:
        raise ValueError("No database URI provided")

    engine: AsyncEngine = create_async_engine(url, echo=True)
    session_factory: async_sessionmaker = async_sessionmaker(
        bind=engine, expire_on_commit=False)

    async def get_session() -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            yield session

    return get_session


def sync_session(url: str | None, scopefunc: Callable) -> scoped_session:

    if not url:
        raise ValueError("No database URI provided")

    engine = create_engine(url, future=True, echo=True)
    session_factory: scoped_session = scoped_session(sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=False
    ), scopefunc=scopefunc)

    return session_factory
