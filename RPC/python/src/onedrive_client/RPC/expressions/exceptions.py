"""Expressions-related expressions."""
__all__ = [
    'Error',
    'ExpressionSyntaxError',
    'UnknownVariable'
]


class Error(Exception):
    """Base error."""
    pass


class ExpressionSyntaxError(Error):
    """Malformed expression syntax."""
    pass


class UnknownVariable(Error):
    """Value of the variable used in the expression is not known."""
    pass
