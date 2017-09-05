"""Provides exceptions used in the ``transport`` package."""

__all__ = [
    'TransportError',
    'TransportConnectionError',
    'UnknownIdentity',
    'NoMessagesError',
    'Closed'
]


class TransportError(Exception):
    """General transport-related error."""
    pass


class Closed(TransportError):
    pass


class TransportConnectionError(TransportError):
    """Connection-related error."""
    pass


class UnknownIdentity(TransportError):
    """Operation for unknown connection was invoked."""
    pass


class NoMessagesError(TransportError):
    """There is no received messages."""
    pass
