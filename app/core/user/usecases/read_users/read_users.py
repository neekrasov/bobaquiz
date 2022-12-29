from ...protocols.dao import UserDAOReader
from ...entities.user import UserEntity, Email, UserID


class UserReaderService:
    def __init__(self, user_reader_dao: UserDAOReader):
        self.user_reader_dao = user_reader_dao

    async def find_user_by_email(self, email: Email) -> UserEntity | None:
        return await self.user_reader_dao.get_user_by_email(email)

    async def find_user_by_id(self, user_id: UserID) -> UserEntity | None:
        return await self.user_reader_dao.get_user_by_id(user_id)
