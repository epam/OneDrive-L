"""Provides abstract Transport base class."""
import abc
from types import TracebackType
from typing import Callable, Generic, List, Optional, Sequence, TypeVar


Address = TypeVar('Address')  # pylint: disable=invalid-name


class Transport(Generic[Address], metaclass=abc.ABCMeta):
    """Message-oriented connection between one or many peers.

    For more information refer to:

        RPC/proto/onedrive_client/RPC/RPC.proto

    """
    @abc.abstractmethod
    def serve(self, address: Address) -> None:
        """Binds a transport-instance to an address."""
        raise NotImplementedError

    @abc.abstractmethod
    def on_inbound_connection(self, callback: Callable[[str], None]) -> None:
        """Set a callback that will be executed when someone connects."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def inbound_connections(self) -> List[str]:
        """List of inbound connection with peers."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def identity(self) -> Optional[str]:
        """Identity associated with the instance."""
        raise NotImplementedError

    @abc.abstractmethod
    def connect(self, address: Address) -> str:
        """Connect to a remote peer."""
        raise NotImplementedError

    @abc.abstractmethod
    def disconnect(self, identity) -> List[str]:
        """Disconnect remote peer."""
        raise NotImplementedError

    @abc.abstractmethod
    def on_connection_lost(
        self,
        callback: Callable[
            [
                str,
                Optional[type],
                Optional[Exception],
                Optional[TracebackType]
            ],
            None
        ]
    ) -> None:
        """Set a callback that will be executed when a disconnect happens.

        If a disconnect happened because of an exception - information about
        the exception is passed as three optional arguments that are the
        same as the info returned by ``sys.exc_info()``.
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def outbound_connections(self) -> List[str]:
        """List of outbound connection with peers."""
        raise NotImplementedError

    @property
    def connections(self) -> List[str]:
        """List of inbound and outbound connection with peers."""
        return self.inbound_connections + self.outbound_connections

    @abc.abstractmethod
    def close(self) -> None:
        """Close the transport, disconnect all the peers."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def is_closed(self) -> bool:
        """Whether the instance is is_closed."""
        raise NotImplementedError

    @abc.abstractmethod
    def send(
        self,
        data: bytes,
        identities: Sequence[str],
        block: bool = True,
        timeout: Optional[float] = None
    ) -> Optional[List[str]]:
        """Send a message to a remote peer.

        If some of the peers identified by 'identities' are disconnected,
        they must be skipped.

        The identities to which sending was successful must be returned in
        case if 'block' is ``True``.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def on_receive(
        self,
        callback: Callable[[str, bytes], None],
    ):
        """Register a 'callback' to be called when data is received.

        The 'callback' is called with two positional arguments: the sender
        identity and the data.
        """
        raise NotImplementedError
