from redis.asyncio import Redis
from datetime import timedelta

from app.core.user.exceptions.auth import TokenDoesNotExist
from app.core.user.protocols.dao import AuthDAO


class AuthDAOImpl(AuthDAO):
    def __init__(self, redis: Redis):
        self._redis = redis

    async def save_refresh_token(
        self,
        token: str,
        session_id: str,
        refresh_token_expire: timedelta
    ) -> None:
        await self._redis.set(
            name=session_id,
            value=token,
            ex=refresh_token_expire
        )

    async def delete_token_if_exists(self, session_id: str) -> None:
        if not await self._redis.exists(session_id):
            raise TokenDoesNotExist
        await self._redis.delete(session_id)
