from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.db import SQLAlchemyUserDatabase

from app.infrastructure.db.models.user import User
from app.api.di.stubs import provide_session_stub


async def provide_user_db(
    session: AsyncSession = Depends(provide_session_stub),
) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    yield SQLAlchemyUserDatabase(session, User)
