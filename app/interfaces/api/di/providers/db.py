from typing import AsyncGenerator, Callable, Type
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.db import SQLAlchemyUserDatabase

from app.infrastructure.db.dao.base import BaseDAO
from app.infrastructure.db.models.user import User
from ...di.stubs import provide_session_stub


async def provide_user_db(
    session: AsyncSession = Depends(provide_session_stub),
) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    yield SQLAlchemyUserDatabase(session, User)


def get_dao(
    dao_type: Type[BaseDAO],
) -> Callable[[AsyncSession], BaseDAO]:
    def _get_dao(
        session: AsyncSession = Depends(provide_session_stub),
    ) -> BaseDAO:
        return dao_type(session=session)

    return _get_dao