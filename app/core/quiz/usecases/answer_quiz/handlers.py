from decimal import Decimal
from app.shared import CommandHandler, Mediator

from ...entity import QuizEntity, QuestionType, QuestionEntity
from ...protocols.dao import QuizDAOReader
from ...dto.quiz_answer import QuizSolution, QuestionSolution
from .events import QuizSolutionValidatedEvent
from ...exceptions import (
    QuizNotFoundException,
    QuestionNotFoundException,
    AnsOptionNotFoundException,
)


class ValidateQuizSolutionCommandHandler(CommandHandler):
    def __init__(self, mediator: Mediator, quiz_dao_reader: QuizDAOReader):
        self._mediator = mediator
        self._quiz_dao_reader = quiz_dao_reader

    async def execute(self, command) -> None:
        quiz_solution: QuizSolution = command.solution
        quiz = await self._quiz_dao_reader.get_quiz_by_id(
            quiz_solution.quiz_id
        )

        if not quiz:
            raise QuizNotFoundException(quiz_solution.quiz_id)

        await self._mediator.publish_event(
            QuizSolutionValidatedEvent(
                user_id=command.user_id,
                solution=self._get_graded_quiz(quiz_solution, quiz),
            )
        )

    def _get_graded_quiz(
        self, quiz_solution: QuizSolution, quiz: QuizEntity
    ) -> QuizSolution:
        quiz_grade = 0.0
        for q_solution in quiz_solution.questions:
            question = quiz.get_question(q_solution.question_id)

            if question is None:
                raise QuestionNotFoundException(q_solution.question_id)

            question_grade = self._get_question_grade(q_solution, question)
            q_solution.grade = Decimal(question_grade)
            quiz_grade += question_grade / len(quiz.questions)

        quiz_solution.grade = Decimal(quiz_grade)
        return quiz_solution

    def _get_question_grade(
        self, q_solution: QuestionSolution, question: QuestionEntity
    ) -> float:
        question_grade = 0.0
        if self.is_nothing_question(question):
            return 1.0
        for ans_solution in q_solution.options:
            answer = question.get_option(ans_solution.ans_option_id)

            if answer is None:
                raise AnsOptionNotFoundException(ans_solution.ans_option_id)

            if question.type == QuestionType.SINGLE:
                if answer.is_correct:
                    question_grade = 1.0
                    ans_solution.is_correct = True
                else:
                    ans_solution.is_correct = False
                    break
            elif question.type == QuestionType.MULTIPLE:
                if answer.is_correct:
                    question_grade += 1 / question.correct_count
                    ans_solution.is_correct = True
                else:
                    ans_solution.is_correct = False

        return question_grade

    def is_nothing_question(self, question: QuestionEntity) -> bool:
        return (
            question.type == QuestionType.NOTHING
            and len(question.options) == 0
        )
