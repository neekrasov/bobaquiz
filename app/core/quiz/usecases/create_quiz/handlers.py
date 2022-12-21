from app.shared import CommandHandler, Mediator
from app.core.quiz.protocols.dao import QuizDAO
from app.core.quiz.entity import (
    QuizEntity,
    QuestionEntity,
    AnsOptionEntity,
    QuestionType,
)
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
            created_at=None,
            **quiz.dict(exclude={"questions"})
        )

        if quiz.questions is None:
            await self._quiz_dao.commit()
            return

        for question in quiz.questions:
            question_id = QuestionEntity.generate_id()
            if question.options is None:
                await self._quiz_dao.commit()
                return

            correct_count = 0
            if question.type == QuestionType.SINGLE:
                correct_count = 1

            question_options = []
            for option in question.options:
                if all(
                    (option.is_correct, question.type == QuestionType.MULTIPLE)
                ):
                    correct_count += 1

                option_in_db = AnsOptionEntity(
                    id=AnsOptionEntity.generate_id(),
                    question_id=question_id,
                    **option.dict()
                )
                question_options.append(option_in_db)

            quiz_in_db.questions.append(
                QuestionEntity(
                    id=question_id,
                    quiz_id=quiz_id,
                    correct_count=correct_count,
                    options=question_options,
                    **question.dict(exclude={"options"})
                )
            )

        await self._quiz_dao.add_quiz(quiz_in_db)
        await self._quiz_dao.commit()
