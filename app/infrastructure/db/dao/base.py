from sqlalchemy.ext.asyncio import AsyncSession
from app.shared import DAO


class BaseDAO(DAO):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    async def flush(self) -> None:
        await self._session.flush()
