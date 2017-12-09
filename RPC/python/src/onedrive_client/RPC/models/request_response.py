"""AUTO-GENERATED WITH PROTOCOL BUFFERS COMPILER. DO NOT EDIT BY HAND.

For descriptions and comments refer to:

    onedrive_client/RPC/RPC.proto
"""
import enum

from onedrive_client.RPC.models import Model, Action
# pylint: disable=missing-docstring,line-too-long


class RequestResponse(Model):
    ID = 'REQUEST_RESPONSE'
    SINGLETON_SESSION = False

    class LocalState(enum.Enum):
        IDLE = 'IDLE'
        IN_PROGRESS = 'IN_PROGRESS'
        CLOSED = 'CLOSED'

    LOCAL_BEGIN = LocalState['IDLE']
    LOCAL_END = LocalState['CLOSED']
    LOCAL_TRANSITIONS = [
        Model.Transition(
            name='Wait for the new peer.',
            condition='NEW_INBOUND_PEER or NEW_OUTBOUND_PEER',
            sources=set([
                LocalState['IDLE']
            ]),
            destination=LocalState['IN_PROGRESS'],
            actions=set([
            ])
        ),
        Model.Transition(
            name='Reject other peers.',
            condition='NEW_INBOUND_PEER or NEW_OUTBOUND_PEER',
            sources=set([
                LocalState['IN_PROGRESS']
            ]),
            destination=Model.ANY,
            actions=set([
                Action['REJECT']
            ])
        ),
        Model.Transition(
            name='Close when the peer is gone.',
            condition='PEER_GONE',
            sources=set([
                LocalState['IN_PROGRESS']
            ]),
            destination=LocalState['CLOSED'],
            actions=set([
            ])
        ),
        Model.Transition(
            name='Close when the endpoint is closed.',
            condition='CLOSE or OUTBOUND_CLOSE',
            sources=set([
                Model.ANY
            ]),
            destination=LocalState['CLOSED'],
            actions=set([
            ])
        )
    ]

    class LocalStateEvent(enum.Enum):
        IDLE = 'LOCAL_IDLE'
        IN_PROGRESS = 'LOCAL_IN_PROGRESS'
        CLOSED = 'LOCAL_CLOSED'

    class RemoteState(enum.Enum):
        IDLE = 'IDLE'
        AWAITING_INBOUND_RESPONSE = 'AWAITING_INBOUND_RESPONSE'
        AWAITING_OUTBOUND_RESPONSE = 'AWAITING_OUTBOUND_RESPONSE'
        AWAITING_INBOUND_CLOSE = 'AWAITING_INBOUND_CLOSE'
        CLOSED = 'CLOSED'

    REMOTE_BEGIN = RemoteState['IDLE']
    REMOTE_END = RemoteState['CLOSED']
    REMOTE_TRANSITIONS = [
        Model.Transition(
            name='Send request',
            condition='OUTBOUND_PAYLOAD and TO_ONE and not OUTBOUND_CLOSE',
            sources=set([
                RemoteState['IDLE']
            ]),
            destination=RemoteState['AWAITING_INBOUND_RESPONSE'],
            actions=set([
                Action['SEND_TO_ONE'],
                Action['SEND_PAYLOAD'],
                Action['REQUIRE_ACKNOWLEDGEMENT']
            ])
        ),
        Model.Transition(
            name='Receive the response.',
            condition='INBOUND_PAYLOAD and REQUIRES_ACKNOWLEDGEMENT and not INBOUND_CLOSE',
            sources=set([
                RemoteState['AWAITING_INBOUND_RESPONSE']
            ]),
            destination=RemoteState['CLOSED'],
            actions=set([
                Action['PROCESS_INBOUND_PAYLOAD'],
                Action['SEND_CLOSE'],
                Action['SEND_REPLY'],
                Action['REQUIRE_ACKNOWLEDGEMENT']
            ])
        ),
        Model.Transition(
            name='Receive the request.',
            condition='INBOUND_INITIAL and INBOUND_PAYLOAD and REQUIRES_ACKNOWLEDGEMENT and not INBOUND_CLOSE',
            sources=set([
                RemoteState['IDLE']
            ]),
            destination=RemoteState['AWAITING_OUTBOUND_RESPONSE'],
            actions=set([
                Action['PROCESS_INBOUND_PAYLOAD']
            ])
        ),
        Model.Transition(
            name='Send response.',
            condition='OUTBOUND_PAYLOAD and not OUTBOUND_CLOSE',
            sources=set([
                RemoteState['AWAITING_OUTBOUND_RESPONSE']
            ]),
            destination=RemoteState['AWAITING_INBOUND_CLOSE'],
            actions=set([
                Action['SEND_TO_ALL'],
                Action['SEND_PAYLOAD'],
                Action['REQUIRE_ACKNOWLEDGEMENT']
            ])
        ),
        Model.Transition(
            name='Inbound close.',
            condition='(INBOUND_CLOSE or LOCAL_CLOSED) and REQUIRES_ACKNOWLEDGEMENT',
            sources=set([
                Model.ANY
            ]),
            destination=RemoteState['CLOSED'],
            actions=set([
            ])
        ),
        Model.Transition(
            name='Outbound close.',
            condition='(OUTBOUND_CLOSE or LOCAL_CLOSED)',
            sources=set([
                RemoteState['AWAITING_INBOUND_RESPONSE'],
                RemoteState['AWAITING_OUTBOUND_RESPONSE']
            ]),
            destination=RemoteState['CLOSED'],
            actions=set([
                Action['SEND_TO_ALL'],
                Action['SEND_CLOSE'],
                Action['REQUIRE_ACKNOWLEDGEMENT']
            ])
        )
    ]
