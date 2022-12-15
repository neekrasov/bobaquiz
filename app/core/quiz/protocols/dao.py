from typing import Protocol
from app.shared.dao import DAO

from app.core.quiz.entity.ans_option import AnsOptionEntity
from app.core.quiz.entity.question import QuestionEntity
from app.core.quiz.entity.quiz import QuizEntity


class QuizDAO(DAO, Protocol):
    async def add_quiz(self, quiz: QuizEntity) -> QuizEntity:
        ...


class QuestionDAO(DAO, Protocol):
    async def add_question(self, question: QuestionEntity) -> QuestionEntity:
        ...


class AnsOptionDAO(DAO, Protocol):
    async def add_answer(self, answer: AnsOptionEntity) -> AnsOptionEntity:
        ...
