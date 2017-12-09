"""Tests for ``onedrive_client.RPC.models.base`` module."""
import enum

import pytest

from onedrive_client.RPC.models.base import Action, Event, Model
from onedrive_client.RPC.models.exceptions import UnrecognizedEventsSet
# pylint: disable=no-self-use


class TestModel:
    """Tests for ``Model`` class."""
    # pylint: disable=invalid-name
    def test_simple_move(self, SimpleModel):
        """Test of simple transitioning of state machines.

        In response to provided current state and input events both state
        machines should be moved to the correct state and emit the correct
        actions.
        """
        model = SimpleModel()

        expected_local_state = model.LocalState['FOO']
        current_local_state = model.LOCAL_BEGIN
        actual_state, actual_actions = model.execute_local(
            current_local_state,
            {Event.NEW_INBOUND_PEER}
        )

        assert actual_state == expected_local_state
        assert actual_actions == {Action.SEND_ERROR}

        current_local_state = actual_state

        expected_remote_state = model.RemoteState['FOO']
        current_remote_state = model.REMOTE_BEGIN
        actual_state, actual_actions = model.execute_remote(
            current_local_state=current_local_state,
            current_remote_state=current_remote_state,
            events={Event.INBOUND_INITIAL}
        )

        assert actual_state == expected_remote_state
        assert actual_actions == {Action.SEND_ERROR}

    def test_unrecognized_events(self, SimpleModel):
        """Exception is raised for events unspecified in the state machines."""
        model = SimpleModel()

        current_local_state = model.LOCAL_BEGIN
        with pytest.raises(UnrecognizedEventsSet):
            model.execute_local(current_local_state, {Event.PEER_GONE})

        current_remote_state = model.REMOTE_BEGIN
        with pytest.raises(UnrecognizedEventsSet):
            model.execute_remote(
                model.LOCAL_BEGIN,
                current_remote_state,
                {Event.INBOUND_CLOSE}
            )

    def test_transition_with_any_source(self, StarSourceModel):
        """Transitions with 'ANY' sources match any input state."""
        model = StarSourceModel()

        for current_state in [model.LocalState.IDLE, model.LocalState.FOO]:
            actual_state, actual_actions = model.execute_local(
                current_state,
                {Event.NEW_INBOUND_PEER}
            )
            assert actual_state == model.LocalState.FOO
            assert actual_actions == {Action.SEND_ERROR}

        for current_state in [model.RemoteState.IDLE, model.RemoteState.FOO]:
            actual_state, actual_actions = model.execute_remote(
                model.LOCAL_BEGIN,
                current_state,
                {Event.INBOUND_INITIAL}
            )
            assert actual_state == model.RemoteState.FOO
            assert actual_actions == {Action.SEND_ERROR}

    def test_transition_with_same_destination(self, StarDestinationModel):
        """Test transitions with the "star" destination.

        Transitions with "star" destination preserve the current state.
        """
        model = StarDestinationModel()

        current_state = StarDestinationModel.LOCAL_BEGIN
        actual_state, actual_actions = model.execute_local(
            current_state,
            {Event.NEW_INBOUND_PEER}
        )
        assert actual_state == current_state
        assert actual_actions == {Action.SEND_ERROR}

        current_state = StarDestinationModel.REMOTE_BEGIN
        actual_state, actual_actions = model.execute_remote(
            actual_state,
            current_state,
            {Event.INBOUND_INITIAL}
        )
        assert actual_state == current_state
        assert actual_actions == {Action.SEND_ERROR}

    def test_transition_with_local_state_events(self, LocalStateEventModel):
        """Test of handling of local state events by remote state machine.

        Remote state machine should additionally receive local state as an
        event.
        """
        model = LocalStateEventModel()

        actual_state, actual_actions = model.execute_remote(
            model.LocalState.FOO,
            model.REMOTE_BEGIN,
            {Event.INBOUND_INITIAL}
        )
        assert actual_state == model.RemoteState.FOO
        assert actual_actions == {Action.SEND_ERROR}

    def test_is_halted(self, SimpleModel):
        """Test of is_halted_*() methods for both state machines."""
        model = SimpleModel()

        assert model.is_halted_local(model.LOCAL_END)
        assert model.is_halted_remote(model.REMOTE_END)

    @pytest.fixture(name='StarDestinationModel')
    def star_destination_model(self):
        """Model with a transition with catch-all destination."""
        # pylint: disable=missing-docstring
        class StarDestinationModel(Model):
            ID = 'STAR_DESTINATION'
            SINGLETON_SESSION = False

            class LocalState(enum.Enum):
                IDLE = 'IDLE'
                FOO = 'FOO'
                CLOSED = 'CLOSED'

            LOCAL_BEGIN = LocalState['IDLE']
            LOCAL_END = LocalState['CLOSED']
            LOCAL_TRANSITIONS = [
                Model.Transition(
                    name='first',
                    condition='NEW_INBOUND_PEER',
                    sources={LOCAL_BEGIN},
                    destination=Model.ANY,
                    actions={Action.SEND_ERROR}
                ),
                Model.Transition(
                    name='second',
                    condition='CLOSE',
                    sources={LocalState.FOO},
                    destination=LOCAL_END,
                    actions={Action.SEND_CLOSE, Action.SEND_TO_ALL}
                )
            ]

            class RemoteState(enum.Enum):
                IDLE = 'IDLE'
                FOO = 'FOO'
                CLOSED = 'CLOSED'

            REMOTE_BEGIN = RemoteState['IDLE']
            REMOTE_END = RemoteState['CLOSED']
            REMOTE_TRANSITIONS = [
                Model.Transition(
                    name='first',
                    condition='INBOUND_INITIAL',
                    sources={REMOTE_BEGIN},
                    destination=Model.ANY,
                    actions={Action.SEND_ERROR}
                ),
                Model.Transition(
                    name='second',
                    condition='CLOSE',
                    sources={RemoteState.FOO},
                    destination=REMOTE_END,
                    actions=set()
                )
            ]

        return StarDestinationModel

    @pytest.fixture(name='StarSourceModel')
    def star_source_model(self):
        """Model with a transition with any source."""
        # pylint: disable=missing-docstring
        class StarSourceModel(Model):
            ID = 'STAR_SOURCE'
            SINGLETON_SESSION = False

            class LocalState(enum.Enum):
                IDLE = 'IDLE'
                FOO = 'FOO'
                CLOSED = 'CLOSED'

            LOCAL_BEGIN = LocalState['IDLE']
            LOCAL_END = LocalState['CLOSED']
            LOCAL_TRANSITIONS = [
                Model.Transition(
                    name='first',
                    condition='NEW_INBOUND_PEER',
                    sources={Model.ANY},
                    destination=LocalState['FOO'],
                    actions={Action.SEND_ERROR}
                ),
                Model.Transition(
                    name='second',
                    condition='CLOSE',
                    sources={Model.ANY},
                    destination=LocalState['CLOSED'],
                    actions={Action.SEND_CLOSE, Action.SEND_TO_ALL}
                )
            ]

            class RemoteState(enum.Enum):
                IDLE = 'IDLE'
                FOO = 'FOO'
                CLOSED = 'CLOSED'

            REMOTE_BEGIN = RemoteState['IDLE']
            REMOTE_END = RemoteState['CLOSED']
            REMOTE_TRANSITIONS = [
                Model.Transition(
                    name='first',
                    condition='INBOUND_INITIAL',
                    sources={Model.ANY},
                    destination=RemoteState['FOO'],
                    actions={Action.SEND_ERROR}
                ),
                Model.Transition(
                    name='second',
                    condition='CLOSE',
                    sources={Model.ANY},
                    destination=RemoteState['CLOSED'],
                    actions=set()
                )
            ]

        return StarSourceModel

    @pytest.fixture(name='SimpleModel')
    def simple_model(self):
        """Simple model."""
        # pylint: disable=missing-docstring
        class SimpleModel(Model):
            ID = 'SIMPLE'
            SINGLETON_SESSION = False

            class LocalState(enum.Enum):
                IDLE = 'IDLE'
                FOO = 'FOO'
                CLOSED = 'CLOSED'

            LOCAL_BEGIN = LocalState['IDLE']
            LOCAL_END = LocalState['CLOSED']
            LOCAL_TRANSITIONS = [
                Model.Transition(
                    name='first',
                    condition='NEW_INBOUND_PEER',
                    sources={LocalState['IDLE']},
                    destination=LocalState['FOO'],
                    actions={Action.SEND_ERROR}
                ),
                Model.Transition(
                    name='second',
                    condition='CLOSE',
                    sources={LocalState['FOO']},
                    destination=LocalState['CLOSED'],
                    actions={Action.SEND_CLOSE, Action.SEND_TO_ALL}
                )
            ]

            class RemoteState(enum.Enum):
                IDLE = 'IDLE'
                FOO = 'FOO'
                CLOSED = 'CLOSED'

            REMOTE_BEGIN = RemoteState['IDLE']
            REMOTE_END = RemoteState['CLOSED']
            REMOTE_TRANSITIONS = [
                Model.Transition(
                    name='first',
                    condition='INBOUND_INITIAL',
                    sources={RemoteState['IDLE']},
                    destination=RemoteState['FOO'],
                    actions={Action.SEND_ERROR}
                ),
                Model.Transition(
                    name='second',
                    condition='CLOSE',
                    sources={RemoteState['FOO']},
                    destination=RemoteState['CLOSED'],
                    actions=set()
                )
            ]

        return SimpleModel

    @pytest.fixture(name='LocalStateEventModel')
    def local_state_event_model(self):
        """Model that uses local-state-events in remote transition(s)."""
        # pylint: disable=missing-docstring
        class LocalStateEventModel(Model):
            """Model that uses local-state-events in the remote transitions."""
            ID = 'LOCAL_STATE_EVENT'
            SINGLETON_SESSION = False

            class LocalState(enum.Enum):
                IDLE = 'IDLE'
                FOO = 'FOO'
                CLOSED = 'CLOSED'

            LOCAL_BEGIN = LocalState['IDLE']
            LOCAL_END = LocalState['CLOSED']
            LOCAL_TRANSITIONS = [
                Model.Transition(
                    name='first',
                    condition='NEW_INBOUND_PEER',
                    sources={LocalState['IDLE']},
                    destination=LocalState['FOO'],
                    actions={Action.SEND_ERROR}
                ),
                Model.Transition(
                    name='second',
                    condition='CLOSE',
                    sources={LocalState['FOO']},
                    destination=LocalState['CLOSED'],
                    actions={Action.SEND_CLOSE, Action.SEND_TO_ALL}
                )
            ]

            class RemoteState(enum.Enum):
                IDLE = 'IDLE'
                FOO = 'FOO'
                CLOSED = 'CLOSED'

            REMOTE_BEGIN = RemoteState['IDLE']
            REMOTE_END = RemoteState['CLOSED']
            REMOTE_TRANSITIONS = [
                Model.Transition(
                    name='first',
                    condition='INBOUND_INITIAL and LOCAL_FOO',
                    sources={RemoteState['IDLE']},
                    destination=RemoteState['FOO'],
                    actions={Action.SEND_ERROR}
                ),
                Model.Transition(
                    name='second',
                    condition='CLOSE',
                    sources={RemoteState['FOO']},
                    destination=RemoteState['CLOSED'],
                    actions=set()
                )
            ]

        return LocalStateEventModel
