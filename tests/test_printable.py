# tests/test_printable.py
from vulcan_logger.printable import Printable


def test_empty_class():
    """
    Test that an instance of a class with no attributes, when inheriting from Printable,
    returns the class name with an empty dictionary as its representation.
    """

    class Empty(Printable):
        pass

    obj = Empty()
    expected_output = "Empty({})"
    assert str(
        obj) == expected_output, f"Expected {expected_output}, got {str(obj)}"
    assert repr(
        obj) == expected_output, f"Expected {expected_output}, got {repr(obj)}"


def test_single_attribute_class():
    """
    Test that an instance of a class with one attribute, when inheriting from Printable,
    returns the correct string representation with that attribute shown.
    """

    class SingleAttribute(Printable):
        def __init__(self, value: int):
            self.value = value

    value = 10
    obj = SingleAttribute(value)
    expected_output = f"SingleAttribute({{'value': {value}}})"
    assert str(
        obj) == expected_output, f"Expected {expected_output}, got {str(obj)}"
    assert repr(
        obj) == expected_output, f"Expected {expected_output}, got {repr(obj)}"


def test_multiple_attributes_class():
    """
    Test that an instance of a class with multiple attributes, when inheriting from Printable,
    returns the correct string representation with all attributes shown.
    """

    class MultipleAttributes(Printable):
        def __init__(self, name: str, age: int):
            self.name = name
            self.age = age

    name = "Jacob"
    age = 30
    obj = MultipleAttributes(name, age)
    expected_output = f"MultipleAttributes({{'name': '{name}', 'age': {age}}})"
    assert str(
        obj) == expected_output, f"Expected {expected_output}, got {str(obj)}"
    assert repr(
        obj) == expected_output, f"Expected {expected_output}, got {repr(obj)}"


def test_inheritance_and_overriding():
    """
    Test that a class which inherits from Printable and also overrides __str__ or __repr__
    uses the overridden methods rather than those from Printable.
    """

    class OverriddenMethods(Printable):
        def __init__(self, value: int):
            self.value = value

        def __repr__(self) -> str:
            return "OverriddenRepresentation"

        def __str__(self) -> str:
            return "OverriddenString"

    obj = OverriddenMethods(100)
    assert str(
        obj) == "OverriddenString", f"Expected 'OverriddenString', got {str(obj)}"
    assert repr(
        obj) == "OverriddenRepresentation", f"Expected 'OverriddenRepresentation', got {repr(obj)}"
