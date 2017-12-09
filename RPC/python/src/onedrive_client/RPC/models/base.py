"""Provides ``Model`` class."""
import enum
from typing import (
    ClassVar,
    Generic,
    GenericMeta,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union
)
from .exceptions import (
    AmbiguousTransitions,
    Halted,
    InconsistentModel,
    UnrecognizedEventsSet
)
from ..expressions import evaluate, get_variables, UnknownVariable
from ..RPC_pb2 import (
    Action as _Action,
    Event as _Event,
    local,
    remote
)


def _get_scope(name, descriptor):
    options = descriptor.values_by_name[name].GetOptions()
    return options.Extensions[local], options.Extensions[remote]


class Event(enum.IntEnum):
    """Represents events used in communication models."""
    # pylint: disable=exec-used
    exec('\n'.join(
        '{} = {}'. format(v.name, v.number)
        for v in _Event.DESCRIPTOR.values
    ), globals(), locals())

    @property
    def is_local(self):
        return _get_scope(self.name, _Event.DESCRIPTOR)[0]

    @property
    def is_remote(self):
        return _get_scope(self.name, _Event.DESCRIPTOR)[1]


class Action(enum.IntEnum):
    """Represents actions used in communication models."""
    # pylint: disable=exec-used
    exec('\n'.join(
        '{} = {}'. format(v.name, v.number)
        for v in _Action.DESCRIPTOR.values
    ), globals(), locals())

    @property
    def is_local(self):
        return _get_scope(self.name, _Action.DESCRIPTOR)[0]

    @property
    def is_remote(self):
        return _get_scope(self.name, _Action.DESCRIPTOR)[1]


LS = TypeVar('LS', bound=enum.Enum)
RS = TypeVar('RS', bound=enum.Enum)


class ModelMeta(GenericMeta):
    """Metaclass for ``Model`` class. Validates correctness of the model."""
    __MODEL_CLASS_CREATED = False
    __LOCAL_PREFIX = 'LOCAL_'

    # pylint: disable=invalid-name,signature-differs,arguments-differ

    def __new__(mcs, name, bases, attributes, **kwargs):
        model_cls: Model = super().__new__(
            mcs,
            name,
            bases,
            attributes,
            **kwargs
        )

        if mcs.__MODEL_CLASS_CREATED:
            LocalStateEvent = enum.Enum(
                'LocalStateEvent',
                {mcs.__LOCAL_PREFIX + s.name: mcs.__LOCAL_PREFIX + s.name
                 for s in model_cls.LocalState}
            )
            model_cls.LocalStateEvent = LocalStateEvent
            mcs.__validate_state_machine(
                states=model_cls.LocalState,
                begin=model_cls.LOCAL_BEGIN,
                end=model_cls.LOCAL_END,
                transitions=model_cls.LOCAL_TRANSITIONS,
                is_local=True,
                is_remote=False,
                any_value=model_cls.ANY,
            )
            mcs.__validate_state_machine(
                states=model_cls.RemoteState,
                begin=model_cls.REMOTE_BEGIN,
                end=model_cls.REMOTE_END,
                transitions=model_cls.REMOTE_TRANSITIONS,
                is_local=False,
                is_remote=True,
                any_value=model_cls.ANY,
                local_state_events=model_cls.LocalStateEvent
            )

        else:
            mcs.__MODEL_CLASS_CREATED = True

        return model_cls

    @classmethod
    def __validate_state_machine(
        mcs,
        states,
        begin,
        end,
        transitions,
        is_remote,
        is_local,
        any_value,
        local_state_events=None,
    ):
        """Validates a state machine (remote or local) for consistency."""
        allowed_events = {e.name for e in Event}
        if is_remote:
            allowed_events |= {e.name for e in local_state_events}
        for transition in transitions:
            if transition.destination not in set(states) | {any_value}:
                raise InconsistentModel
            if not transition.sources <= set(states) | {any_value}:
                raise InconsistentModel
            if not get_variables(transition.condition) <= allowed_events:
                raise InconsistentModel
            if not set(transition.actions) <= set(Action):
                raise InconsistentModel
            if is_remote and not all(
                Event[e].is_remote
                for e in get_variables(transition.condition)
                if not e.startswith(mcs.__LOCAL_PREFIX)
            ):
                raise InconsistentModel
            if is_remote and not all(
                action.is_remote
                for action in transition.actions
            ):
                raise InconsistentModel
            if is_local and not all(
                Event[e].is_local
                for e in get_variables(transition.condition)
            ):
                raise InconsistentModel
            if is_local and not all(
                action.is_local
                for action in transition.actions
            ):
                raise InconsistentModel

        if not any(any_value in t.sources or begin in t.sources
                   for t in transitions):
            raise InconsistentModel

        if not any(end == t.destination for t in transitions):
            raise InconsistentModel


class Model(Generic[LS, RS], metaclass=ModelMeta):
    """Represents communication model."""
    ANY = '*'

    class Transition(NamedTuple):
        """Represents state machine's transition."""
        name:        str
        condition:   str
        sources:     Set[Union[LS, RS]]
        destination: Union[LS, RS, str]
        actions:     Set[Action]

    ID: str
    SINGLETON_SESSION: bool

    LocalState:         ClassVar[Type[LS]]
    LOCAL_BEGIN:        ClassVar['LocalState']
    LOCAL_END:          ClassVar['LocalState']
    LOCAL_TRANSITIONS:  ClassVar[List[Transition]]

    RemoteState:        ClassVar[Type[RS]]
    LocalStateEvent:    ClassVar[enum.Enum]
    REMOTE_BEGIN:       ClassVar['RemoteState']
    REMOTE_END:         ClassVar['RemoteState']
    REMOTE_TRANSITIONS: ClassVar[List[Transition]]

    @classmethod
    def __execute(
        cls,
        states: Type[enum.Enum],
        end: Union[LS, RS],
        current_state: Union[LS, RS],
        transitions: Sequence[Transition],
        events: Set[Event]
    ) -> Tuple[Union[LS, RS], Set[Action]]:
        """Execute generic state machine - local or remote."""
        if current_state not in states:
            raise InconsistentModel

        if current_state == end:
            raise Halted

        matched = []
        for transition in transitions:
            if (current_state not in transition.sources and
                cls.ANY not in transition.sources):
                continue

            variables = dict.fromkeys([e.name for e in events], True)
            try:
                is_condition_satisfied = evaluate(
                    transition.condition,
                    variables,
                    False
                )
            except UnknownVariable:
                continue

            if not is_condition_satisfied:
                continue

            matched.append(transition)

        if len(matched) == 0:
            raise UnrecognizedEventsSet(events)
        elif len(matched) > 1:
            raise AmbiguousTransitions(matched)

        matched_transition = matched[0]
        next_state = current_state
        if matched_transition.destination != cls.ANY:
            next_state = matched_transition.destination

        return next_state, matched_transition.actions

    @classmethod
    def is_halted_local(cls, state):
        """Is local state machine halted."""
        return state == cls.LOCAL_END

    @classmethod
    def is_halted_remote(cls, state):
        """Is remote state machine halted."""
        return state == cls.REMOTE_END

    def execute_local(
        self,
        current_state: 'LocalState',
        events: Set[Event]
    ) -> Tuple[LS, Set[Action]]:
        """Execute local state machine."""
        if not all(e.is_local for e in events):
            raise ValueError
        return self.__execute(
            states=self.LocalState,
            end=self.LOCAL_END,
            current_state=current_state,
            transitions=self.LOCAL_TRANSITIONS,
            events=events
        )

    def execute_remote(
        self,
        current_local_state: 'RemoteState',
        current_remote_state: 'LocalState',
        events: Set[Event]
    ) -> Tuple[RS, Set[Action]]:
        """Execute local state machine."""
        if not all(e.is_remote for e in events):
            raise ValueError
        local_state_event = self.LocalStateEvent[
            'LOCAL_' + current_local_state.name
        ]
        events.add(local_state_event)
        return self.__execute(
            states=self.RemoteState,
            end=self.REMOTE_END,
            current_state=current_remote_state,
            transitions=self.REMOTE_TRANSITIONS,
            events=events
        )


_MODEL_REGISTRY = {}


def register_model(model_cls: Type[Model]):
    _MODEL_REGISTRY[model_cls.ID] = model_cls


def get_model(model_id) -> Optional[Type[Model]]:
    return _MODEL_REGISTRY.get(model_id)
