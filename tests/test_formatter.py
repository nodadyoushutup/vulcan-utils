# tests/test_formatter.py
import pytest
from vulcan_logger.formatter import Formatter


@pytest.mark.parametrize("milliseconds, expected", [
    (3901023, "1h 5m 1s 23ms"),
    (90061023, "1d 1h 1m 1s 23ms"),
    (31556952000, "1y 5h 49m 12s"),  # Corrected expected value
    (0, "")
])
def test_formatter_duration_to_string(milliseconds: int, expected: str) -> None:
    """
    Test the Formatter class to ensure it accurately formats durations as strings.

    Args:
        milliseconds (int): The duration in milliseconds to format.
        expected (str): The expected formatted string.

    Verifies that the `duration` method returns a correctly formatted string based on the provided milliseconds.
    """

    formatter = Formatter()
    result = formatter.duration(milliseconds, format_type=str, delimiter=" ")
    assert result == expected, f"Expected {expected}, got {result}"


@pytest.mark.parametrize("milliseconds, expected", [
    (3901023, [("hours", 1), ("minutes", 5),
     ("seconds", 1), ("milliseconds", 23)]),
    (90061023, [("days", 1), ("hours", 1), ("minutes", 1),
     ("seconds", 1), ("milliseconds", 23)]),
    # Corrected expected value
    (31556952000, [("years", 1), ("hours", 5),
     ("minutes", 49), ("seconds", 12)]),
    (0, [])
])
def test_formatter_duration_to_list(milliseconds: int, expected: list) -> None:
    """
    Test the Formatter class to ensure it accurately formats durations as lists of tuples.

    Args:
        milliseconds (int): The duration in milliseconds to format.
        expected (list): The expected list of tuples representing the duration.

    Verifies that the `duration` method returns a list of tuples with correctly formatted duration components.
    """

    formatter = Formatter()
    result = formatter.duration(milliseconds, format_type=list)
    assert result == expected, f"Expected {expected}, got {result}"


@pytest.mark.parametrize("milliseconds, expected", [
    (3901023, {"hours": 1, "minutes": 5, "seconds": 1, "milliseconds": 23}),
    (90061023, {"days": 1, "hours": 1, "minutes": 1,
     "seconds": 1, "milliseconds": 23}),
    # Corrected expected value
    (31556952000, {"years": 1, "hours": 5, "minutes": 49, "seconds": 12}),
    (0, {})
])
def test_formatter_duration_to_dict(milliseconds: int, expected: dict) -> None:
    """
    Test the Formatter class to ensure it accurately formats durations as dictionaries.

    Args:
        milliseconds (int): The duration in milliseconds to format.
        expected (dict): The expected dictionary with duration components.

    Verifies that the `duration` method returns a dictionary with non-zero duration components correctly mapped.
    """

    formatter = Formatter()
    result = formatter.duration(milliseconds, format_type=dict)
    assert result == expected, f"Expected {expected}, got {result}"
