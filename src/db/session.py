from typing import AsyncGenerator, Callable

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def async_session(uri: str | None) -> Callable[..., AsyncGenerator[AsyncSession, None]]:

    if not uri:
        raise ValueError("No database URI provided")

    engine: AsyncEngine = create_async_engine(uri, echo=True)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)  # type: ignore

    async def get_session() -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            yield session

    return get_session


def sync_session(uri: str | None) -> scoped_session:

    if not uri:
        raise ValueError("No database URI provided")

    engine = create_engine(uri, future=True, echo=True)
    session_factory = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)  # type: ignore

    return scoped_session(session_factory)