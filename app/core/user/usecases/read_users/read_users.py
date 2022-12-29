from typing import Sequence
from uuid import UUID
from ...protocols.dao import UserDAOReader
from ...entities.user import UserEntity, Email
from ...exceptions.user import UserIsNotAuthorQuiz


class UserReaderService:
    def __init__(self, user_reader_dao: UserDAOReader):
        self.user_reader_dao = user_reader_dao

    async def find_user_by_email(self, email: Email) -> UserEntity | None:
        return await self.user_reader_dao.get_user_by_email(email)

    async def find_user_by_id(self, user_id: UUID) -> UserEntity | None:
        return await self.user_reader_dao.get_user_by_id(user_id)

    async def get_users_completed_quiz(
        self, quiz_id: UUID, author: UserEntity
    ) -> Sequence[UserEntity]:
        authorship_status = await self.user_reader_dao.check_author_quiz(
            quiz_id=quiz_id,
            author_id=author.id
        )
        if not authorship_status:
            raise UserIsNotAuthorQuiz("Quiz not found or user is not author")

        users = await self.user_reader_dao.get_users_completed_quiz(quiz_id)
        return users
