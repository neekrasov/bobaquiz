from uuid import UUID
from pydantic import BaseModel


class AnsOptionSolutionRequest(BaseModel):
    ans_option_id: UUID


class QuestionSolutionRequest(BaseModel):
    question_id: UUID
    options: list[AnsOptionSolutionRequest]


class QuizSolutionRequest(BaseModel):
    quiz_id: UUID
    questions: list[QuestionSolutionRequest]
