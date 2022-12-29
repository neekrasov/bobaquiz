from app.shared import DTO
from datetime import datetime
from ..entities.user import Email


class MetaJWT(DTO):
    exp: datetime
    sub: str


class UserJWT(DTO):
    email: Email


class PairTokens(DTO):
    access_token: str
    refresh_token: str
