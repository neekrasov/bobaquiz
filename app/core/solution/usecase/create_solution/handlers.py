from app.shared import EventHandler, Mediator
from ...protocols.dao import QuizSolutionDAO
from ...entity import (
    QuizSolutionEntity,
    QuestionSolutionEntity,
    AnsOptionSolutionEntity,
)


class QuizSolutionValidatedEventHandler(EventHandler):
    def __init__(
        self,
        mediator: Mediator,
        quiz_solution_dao: QuizSolutionDAO,
    ):
        self._mediator = mediator
        self._quiz_solution_dao = quiz_solution_dao

    async def execute(self, event):
        quiz_solution = event.solution
        quiz_solution_id = QuizSolutionEntity.generate_id()
        questions = []
        for question in quiz_solution.questions:
            question_solution_id = QuestionSolutionEntity.generate_id()
            options = []
            for option in question.options:
                options.append(
                    AnsOptionSolutionEntity(
                        id=AnsOptionSolutionEntity.generate_id(),
                        ans_option_id=option.ans_option_id,
                        question_solution_id=question_solution_id,
                        is_correct=option.is_correct,
                    )
                )
            questions.append(
                QuestionSolutionEntity(
                    id=QuestionSolutionEntity.generate_id(),
                    question_id=question.question_id,
                    quiz_solution_id=quiz_solution_id,
                    grade=question.grade,
                    options=options,
                )
            )
        await self._quiz_solution_dao.add_quiz_solution(
            QuizSolutionEntity(
                id=quiz_solution_id,
                quiz_id=quiz_solution.quiz_id,
                user_id=event.user_id,
                grade=quiz_solution.grade,
                questions=questions,
            )
        )
        await self._quiz_solution_dao.commit()
