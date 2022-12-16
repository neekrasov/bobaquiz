from app.shared import BaseAppException


class QuizException(BaseAppException):
    """Base quiz exception"""


class QuizNotFoundException(QuizException):
    """Quiz not found exception"""
