from typing import Callable, Type, TypeVar
from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.dao.base import BaseDAO, BaseDAOReader
from app.infrastructure.db.dao.auth import AuthDAOImpl
from ...di.stubs import provide_session_stub, provide_redis_stub

DAO = TypeVar("DAO", BaseDAO, BaseDAOReader)


def get_dao(
    dao_type: Type[DAO],
) -> Callable[[AsyncSession], DAO]:
    def _get_dao(
        session: AsyncSession = Depends(provide_session_stub),
    ) -> DAO:
        return dao_type(session=session)

    return _get_dao


def provide_auth_dao(
    redis: Redis = Depends(provide_redis_stub),
):
    return AuthDAOImpl(redis=redis)
