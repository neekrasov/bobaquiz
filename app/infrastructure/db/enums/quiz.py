from enum import Enum


class QuizType(Enum):
    SURVEY = "survey"
    TEST = "test"


class QuestionType(Enum):
    SINGLE = "single"
    MULTIPLE = "multiple"
