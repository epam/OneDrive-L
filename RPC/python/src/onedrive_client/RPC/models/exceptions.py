"""Models-relates exceptions."""
__all__ = [
    'Error',
    'InconsistentModel',
    'UnrecognizedEventsSet',
    'AmbiguousTransitions',
    'Halted'
]


class Error(Exception):
    pass


class InconsistentModel(Error):
    pass


class UnrecognizedEventsSet(Error):
    pass


class AmbiguousTransitions(Error):
    pass


class Halted(Error):
    pass
