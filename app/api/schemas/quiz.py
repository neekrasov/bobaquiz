from pydantic import BaseModel


class QuizAnswer(BaseModel):
    answer: str
    correct: bool
    img: str


class QuizIn(BaseModel):
    name: str
    ans_options: list[QuizAnswer]
