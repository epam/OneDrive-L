"""Provides basic addition test."""

from storage_service.storage import Data


def test_data():
    """
    Test if data is shared between two singleton instances
    """
    message = 'Object has no required attribute(s)'

    first_inst = Data(first='exists')
    assert hasattr(first_inst, 'first'), message

    test_dict = dict(second='exists')
    second_inst = Data(**test_dict)
    assert hasattr(first_inst, 'second'), message

    assert all(hasattr(second_inst, key) for key in ('first', 'second')), \
        message
    assert all(hasattr(first_inst, key) for key in ('first', 'second')), \
        message
