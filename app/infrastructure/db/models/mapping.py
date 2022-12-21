from .base import Base
from .quiz.quiz import map_quiz_tables
from .solution.solution import map_solution_tables


def start_mapper():
    mapper_registry = Base.registry
    map_quiz_tables(mapper_registry)
    map_solution_tables(mapper_registry)
