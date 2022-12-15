from sqlalchemy.orm import relationship, foreign
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
            "id": quiz_table.c.id,
            "name": quiz_table.c.name,
            "img": quiz_table.c.img,
            "author_id": quiz_table.c.author_id,
            "type": quiz_table.c.type,
            "questions": relationship(
                QuestionEntity,
                cascade="all, delete-orphan",
                overlaps="questions",
            ),
        },
    )
    mapper_registry.map_imperatively(
        QuestionEntity,
        question_table,
        properties={
            "id": question_table.c.id,
            "quiz_id": foreign(question_table.c.quiz_id),
            "name": question_table.c.name,
            "img": question_table.c.img,
            "file": question_table.c.file,
            "type": question_table.c.type,
            "options": relationship(
                AnsOptionEntity,
                cascade="all, delete-orphan",
                passive_deletes=True,
                overlaps="options",
            )
        },
    )
    mapper_registry.map_imperatively(
        AnsOptionEntity,
        ans_option_table,
        properties={
            "id": ans_option_table.c.id,
            "question_id": foreign(ans_option_table.c.question_id),
            "name": ans_option_table.c.name,
            "img": ans_option_table.c.img,
            "file": ans_option_table.c.file,
            "is_correct": ans_option_table.c.is_correct
        },
    )
