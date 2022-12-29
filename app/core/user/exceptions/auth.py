class BaseAuthException(Exception):
    """Base exception for auth errors."""


class TokenDoesNotExist(BaseAuthException):
    """Raised when token does not exist in database."""


class IncorrectUserCredentials(BaseAuthException):
    """Raised when user credentials are incorrect."""


class TokenDecodeError(BaseAuthException):
    """Raised when token can not be decoded."""
