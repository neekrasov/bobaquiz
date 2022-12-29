from app.shared import BaseAppException


class UserException(BaseAppException):
    """Base user exception"""


class UserDoesNotExist(UserException):
    """User does not exist exception"""


class UserAlreadyExists(UserException):
    """User already exists exception"""
