from app.shared import CommandHandler, Mediator
from app.core.quiz.exceptions.quiz import QuizNotFoundException
from app.core.quiz.protocols.dao import QuizDAO, QuizDAOReader
from .commands import PatchQuizCommand


class PatchQuizCommandHandler(CommandHandler):

    def __init__(
        self,
        mediator: Mediator,
        quiz_dao: QuizDAO,
        quiz_dao_reader: QuizDAOReader,
    ):
        self._mediator = mediator
        self._quiz_dao = quiz_dao
        self._quiz_dao_reader = quiz_dao_reader

    async def execute(self, command: PatchQuizCommand) -> None:
        quiz = await self._quiz_dao_reader.get_quiz_by_id(command.quiz_id)

        if not quiz:
            raise QuizNotFoundException("Quiz not found")

        await self._quiz_dao.update_quiz(quiz, command.quiz)
        await self._quiz_dao.flush()
