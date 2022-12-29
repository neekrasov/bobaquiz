from app.shared import DTO
from ..entities.user import HashedPassword, Username, Email


class UserCreate(DTO):
    username: Username
    hashed_password: HashedPassword
    email: Email
    policy: bool
