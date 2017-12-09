"""Peer-level exceptions."""


class PeerError(Exception):
    """Base peer error."""
    pass


class EndpointIsClosed(PeerError):
    """Endpoint is closed, operation is not permitted."""
    pass


class UnknownPeer(PeerError):
    """Remote peer with given identity is not known."""
    pass


class InvalidAction(PeerError):
    """Model produced unacceptable action."""
    pass


class IncompatiblePacket(PeerError):
    """The packet is incompatible."""
    pass


class ServiceNotFound(PeerError):
    """Service or method associated with the method is not found."""
    pass
