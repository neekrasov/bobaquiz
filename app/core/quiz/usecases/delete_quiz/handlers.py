from app.shared import Mediator, CommandHandler
from app.core.quiz.protocols.dao import QuizDAO, QuizDAOReader

from .commands import DeleteQuizCommand
from ...exceptions import QuizNotFoundException


class DeleteQuizCommandHandler(CommandHandler):
    def __init__(
        self,
        mediator: Mediator,
        quiz_dao: QuizDAO,
        quiz_dao_reader: QuizDAOReader,
    ):
        self._mediator = mediator
        self._quiz_dao = quiz_dao
        self._quiz_dao_reader = quiz_dao_reader

    async def execute(self, command: DeleteQuizCommand):

        quiz = await self._quiz_dao_reader.get_quiz_by_id(command.quiz_id)

        if not quiz:
            raise QuizNotFoundException()

        await self._quiz_dao.delete_quiz(
            command.quiz_id, command.author_id
        )
        await self._quiz_dao.commit()
