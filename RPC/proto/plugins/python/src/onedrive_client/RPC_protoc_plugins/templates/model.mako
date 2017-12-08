"""AUTO-GENERATED WITH PROTOCOL BUFFERS COMPILER. DO NOT EDIT BY HAND.

For descriptions and comments refer to:

    ${SOURCE_PATH}
"""
<%!
    import re

    def to_camel_case(text):
        return re.sub(
            r'([A-Za-z]*)([^A-Za-z0-9]|$)',
            lambda match: match.group(1).capitalize(),
            text
        )
%>\
import enum

from onedrive_client.RPC.models import Model, Action
# pylint: disable=missing-docstring,line-too-long


class ${model.name | to_camel_case}(Model):
    ID = ${repr(model.id)}
    SINGLETON_SESSION = ${repr(model.singleton_session)}

    class LocalState(enum.Enum):
% for state in model.local.states:
        ${state} = ${repr(state)}
% endfor

    LOCAL_BEGIN = LocalState[${repr(model.local.begin)}]
    LOCAL_END = LocalState[${repr(model.local.end)}]
    LOCAL_TRANSITIONS = [
% for transition in model.local.transitions:
        Model.Transition(
            name=${repr(transition.name)},
            condition=${repr(transition.condition)},
            sources=set([
% for source in transition.sources:
%if source != '*':
                LocalState[${repr(source)}]\
%else:
                Model.ANY\
%endif
${',' if not loop.last else ''}
% endfor
            ]),
            destination=\
%if transition.destination != '*':
LocalState[${repr(transition.destination)}],
%else:
Model.ANY,
%endif
            actions=set([
% for action in transition.actions:
                Action[${repr(action)}]${',' if not loop.last else ''}
% endfor
            ])
        )${',' if not loop.last else ''}
% endfor
    ]

    class LocalStateEvent(enum.Enum):
% for state in model.local.states:
        ${state} = 'LOCAL_${state}'
% endfor

    class RemoteState(enum.Enum):
% for state in model.remote.states:
        ${state} = ${repr(state)}
% endfor

    REMOTE_BEGIN = RemoteState[${repr(model.remote.begin)}]
    REMOTE_END = RemoteState[${repr(model.remote.end)}]
    REMOTE_TRANSITIONS = [
% for transition in model.remote.transitions:
        Model.Transition(
            name=${repr(transition.name)},
            condition=${repr(transition.condition)},
            sources=set([
% for source in transition.sources:
%if source != '*':
                RemoteState[${repr(source)}]\
%else:
                Model.ANY\
%endif
${',' if not loop.last else ''}
% endfor
            ]),
            destination=\
%if transition.destination != '*':
RemoteState[${repr(transition.destination)}],
%else:
Model.ANY,
%endif
            actions=set([
% for action in transition.actions:
                Action[${repr(action)}]${',' if not loop.last else ''}
% endfor
            ])
        )${',' if not loop.last else ''}
% endfor
    ]
