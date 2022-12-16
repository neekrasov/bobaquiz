from sqlalchemy.orm import relationship
from app.infrastructure.db.models.quiz import (
    Quiz as QuizORM,
    Question as QuestionORM,
    AnsOption as AnsOptionORM,
    Base,
)
from app.core.quiz.entity.quiz import QuizEntity as QuizEntity
from app.core.quiz.entity.question import QuestionEntity as QuestionEntity
from app.core.quiz.entity.ans_option import AnsOptionEntity as AnsOptionEntity


def start_mapper():
    mapper_registry = Base.registry
    quiz_table = QuizORM.__table__
    question_table = QuestionORM.__table__
    ans_option_table = AnsOptionORM.__table__

    mapper_registry.map_imperatively(
        QuizEntity,
        quiz_table,
        properties={
            "questions": relationship(
                QuestionEntity,
                cascade="all, delete-orphan",
            ),
        },
    )
    mapper_registry.map_imperatively(
        QuestionEntity,
        question_table,
        properties={
            "options": relationship(
                AnsOptionEntity,
                cascade="all, delete-orphan",
                lazy="selectin",
            )
        },
    )
    mapper_registry.map_imperatively(
        AnsOptionEntity,
        ans_option_table
    )
