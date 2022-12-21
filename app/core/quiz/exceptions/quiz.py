from app.shared import BaseAppException


class QuizException(BaseAppException):
    """Base quiz exception"""


class QuizNotFoundException(QuizException):
    """Quiz not found exception"""


class QuestionException(BaseAppException):
    """Question not found exception"""


class QuestionNotFoundException(QuestionException):
    """Question not found exception"""


class AnsOptionException(BaseAppException):
    """Answer option not found exception"""


class AnsOptionNotFoundException(AnsOptionException):
    """Answer option not found exception"""
