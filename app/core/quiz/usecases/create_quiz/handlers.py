from app.shared import CommandHandler, Mediator
from app.core.quiz.protocols.dao import QuizDAO
from app.core.quiz.entity import QuizEntity, QuestionEntity, AnsOptionEntity
from .commands import CreateQuizCommand


class CreateQuizCommandHandler(CommandHandler):
    def __init__(
        self,
        mediator: Mediator,
        quiz_dao: QuizDAO,
    ):
        self._mediator = mediator
        self._quiz_dao = quiz_dao

    async def execute(self, command: CreateQuizCommand) -> None:
        quiz = command.quiz
        quiz_id = QuizEntity.generate_id()
        quiz_in_db = QuizEntity(
            id=quiz_id,
            author_id=command.author_id,
            **quiz.dict(exclude={"questions"})
        )

        if quiz.questions is None:
            await self._quiz_dao.commit()
            return

        for question in quiz.questions:
            question_id = QuestionEntity.generate_id()
            question_in_db = QuestionEntity(
                id=question_id,
                quiz_id=quiz_id,
                **question.dict(exclude={"options"})
            )

            if question.options is None:
                await self._quiz_dao.commit()
                return

            for option in question.options:
                option_in_db = AnsOptionEntity(
                    id=AnsOptionEntity.generate_id(),
                    question_id=question_id,
                    **option.dict()
                )
                question_in_db.options.append(option_in_db)

            quiz_in_db.questions.append(question_in_db)

        await self._quiz_dao.add_quiz(quiz_in_db)
        await self._quiz_dao.commit()
