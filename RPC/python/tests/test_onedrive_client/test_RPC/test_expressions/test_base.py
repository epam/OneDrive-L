"""Tests for onedrive_client.RPC.expressions.base module."""
import pytest

from onedrive_client.RPC.expressions import (
    evaluate,
    ExpressionSyntaxError,
    UnknownVariable
)


@pytest.mark.parametrize('expression, variables, expected_result', [
    ('A', {'A': True}, True),
    ('A', {'A': False}, False),
    ('true', {}, True),
    ('false', {}, False),
    ('A and B', {'A': True, 'B': True}, True),
    ('A and B', {'A': True, 'B': False}, False),
    ('A and B', {'A': False, 'B': True}, False),
    ('A and B', {'A': False, 'B': False}, False),
    ('A or B', {'A': True, 'B': True}, True),
    ('A or B', {'A': True, 'B': False}, True),
    ('A or B', {'A': False, 'B': True}, True),
    ('A or B', {'A': False, 'B': False}, False),
    ('not A', {'A': True}, False),
    ('not A', {'A': False}, True),
    ('A and not (B or C) or D and E and F and false',
     {'A': False, 'B': True, 'C': False, 'D': True, 'E': False, 'F': True},
     False)
])
def test_evaluate(expression, variables, expected_result):
    actual_result = evaluate(expression, variables)
    assert actual_result == expected_result


@pytest.mark.parametrize('expression, variables, expected_exception', [
    ('A', {}, UnknownVariable),
    ('A or B', {'A': True}, UnknownVariable),
    ('A B', {'A': True, 'B': True}, ExpressionSyntaxError),
    ('A,', {'A': True}, ExpressionSyntaxError),
    ('!A', {'A': True}, ExpressionSyntaxError),
    ('1A', {'A': True}, ExpressionSyntaxError),
    ('not', {}, ExpressionSyntaxError),
    ('and', {}, ExpressionSyntaxError),
    ('or', {}, ExpressionSyntaxError),
    ('and not', {}, ExpressionSyntaxError),
    ('(', {}, ExpressionSyntaxError),
    (')', {}, ExpressionSyntaxError)
])
def test_evaluate_fail(expression, variables, expected_exception):
    with pytest.raises(expected_exception):
        evaluate(expression, variables)


@pytest.mark.parametrize('expression, variables, default, expected_result', [
    ('A', {}, False, False),
    ('A or B', {'B': True}, False, True),
])
def test_default(expression, variables, default, expected_result):
    actual_result = evaluate(expression, variables, default)
    assert actual_result == expected_result
