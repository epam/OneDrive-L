"""Tests for ``onedrive_client.entities.base`` module."""
import pytest

from tests.proto.test import Bar, Foo
# pylint: disable=blacklisted-name,no-self-use


class TestEntity:
    """Tests for ``Entity`` class."""

    @pytest.fixture
    def foo(self):
        return Foo()

    class TestCompositeField:
        """Tests for composite fields."""

        def test_composite_fields_are_unset_by_default(self, foo: Foo):
            """Composite fields are unset by default.

            Unlike primitive fields which are set by default.
            """
            assert 'composite_field' not in foo

        def test_set_composite_field(self, foo: Foo):
            """Simple case of setting a composite field."""
            expected_value = {'eggs': 1}
            foo['composite_field'] = expected_value

            assert foo['composite_field'] == expected_value
            assert foo['composite_field']['eggs'] == expected_value['eggs']

        def test_composite_fields_are_converted_to_entity_instances(
            self,
            foo: Foo
        ):
            """Composite fields are represented as entity-instances."""
            value = {'eggs': 1}
            foo['composite_field'] = value

            assert foo['composite_field'] == value
            assert isinstance(foo['composite_field'], Bar)

        @pytest.mark.parametrize('value', [
            {'eggs': 'string'},
            {'eggs': 'string', 'sausages': 'string'},
            {'sausages': 0},
            0,
            [0]
        ])
        def test_set_composite_field_wrong_type_fails(self, foo: Foo, value):
            """Error is raised when composite field receives wring value.

            When a composite field is set to a value that violates type
            or structure constraints of it - ``TypeError`` should be raised.
            """
            with pytest.raises(TypeError):
                foo['composite_field'] = value

    class TestRepeatedField:
        """Tests for repeated fields."""

        def test_repeated_field_is_empty_list_by_default(self, foo: Foo):
            """Repeated fields must be set to empty list by default."""
            assert foo['repeated_field'] == []

        def test_append_to_repeated_field(self, foo: Foo):
            """Simple case of appending a new value to a repeated field."""
            expected_value = 'test'
            foo['repeated_field'].append(expected_value)

            assert foo['repeated_field'][0] == expected_value

        @pytest.mark.parametrize('value, expected_value', [
            (['a', 'b', 'c'], ['a', 'b', 'c']),
            (iter(['a', 'b', 'c']), ['a', 'b', 'c'])
        ])
        def test_override_repeated_field(
            self,
            foo: Foo,
            value, expected_value
        ):
            """Repeated fields could be overridden with a new iterable."""
            foo['repeated_field'] = value

            assert foo['repeated_field'] == expected_value

        @pytest.mark.parametrize('value', [0, ['test'], {0: 1}, b'test'])
        def test_append_value_of_wrong_type_to_repeated_field_fails(
            self,
            foo: Foo,
            value
        ):
            """Addition of an invalid value to a repeated field fails."""
            with pytest.raises(TypeError):
                foo['repeated_field'].append(value)

        @pytest.mark.parametrize('value', [
            0, [0], {0: 1}, b'test', [b'test'], ['test', 0]
        ])
        def test_override_repeated_field_with_value_of_wrong_type_fails(
            self,
            foo: Foo,
            value
        ):
            """Assignment of an invalid value to a repeated field fails."""
            with pytest.raises(TypeError):
                foo['repeated_field'] = value

    class TestEnumField:
        """Tests for enum-fields."""
        def test_set_enum_field(self, foo: Foo):
            """Basic assignment to a enum-field."""
            expected_value = 1
            foo['manufacturer'] = expected_value
            assert foo['manufacturer'] == expected_value

        def test_set_sub_enum_field(self, foo: Foo):
            """Basic assignment to a sub-enum-field.

            In this case Enum is is not top-level and defined withing
            a message declaration in the contract.
            """
            expected_value = 1
            foo['sub_enum_field'] = expected_value
            assert foo['sub_enum_field'] == expected_value

        def test_set_enum_field_to_number_not_in_enum_fails(self, foo: Foo):
            """Assignment of a not-belonging number to a enum-field fails."""
            with pytest.raises(TypeError):
                foo['manufacturer'] = 100

        @pytest.mark.parametrize('value', [
            100, [0], {0: 1}, b'test', [b'test'], ['test', 0]
        ])
        def test_set_enum_field_to_wrong_type_value_fails(
            self,
            foo: Foo,
            value
        ):
            """Assignment of an invalid value to a enum-field fails."""
            with pytest.raises(TypeError):
                foo['manufacturer'] = value

    def test_set_regular_field(self, foo: Foo):
        """Basic assignment."""
        expected_value = b'test'
        foo['foo'] = expected_value

        assert foo['foo'] == expected_value

    @pytest.mark.parametrize('value', [0, [0], {'foo': 0}, 'test'])
    def test_set_regular_field_wrong_type_fails(self, foo: Foo, value):
        """Assignment to an invalid value fails."""
        with pytest.raises(TypeError):
            foo['foo'] = value

    def test_set_non_existent_field_fails(self, foo: Foo):
        """Assignment to a non-existent field fails."""
        with pytest.raises(TypeError):
            foo['not_exists'] = 0
