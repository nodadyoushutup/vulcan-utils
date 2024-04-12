import json
import time
from datetime import datetime
from typing import List
from unittest.mock import patch

import pytest

from vulcan_logger.decorator import log, retry, to_json
from vulcan_logger.encoder import Encoder


def _sample_function(x: int, y: int = 2) -> int:
    """
    Simple function that adds two integers.

    Args:
        x (int): The first integer to add.
        y (int): The second integer to add, defaulting to 2.

    Returns:
        int: The sum of x and y.
    """

    return x + y


def _slow_function(delay: float) -> float:
    """
    Function that simulates a delay before returning the delay value. Used to test timing and performance.

    Args:
        delay (float): The duration in seconds for which the function should pause.

    Returns:
        float: The actual delay value used.
    """

    time.sleep(delay)
    return delay


def _failing_function(attempts: List[int], max_attempts: int = 2) -> str:
    """
    Simulates a function that fails a specified number of times before succeeding.
    This function is used primarily to test retry logic in decorators or other error-handling mechanisms.

    Args:
        attempts (List[int]): A list containing a single integer that tracks the number of attempts made so far. 
            This list is modified in-place to increment the count of attempts.
        max_attempts (int): The number of times the function should fail before finally succeeding.

    Returns:
        str: Returns "Success" once the function exceeds the number of allowed failures.

    Raises:
        ValueError: Raises a deliberate exception until the number of failures reaches max_attempts.
    """

    if attempts[0] < max_attempts:
        attempts[0] += 1
        raise ValueError("Deliberate Exception")
    return "Success"


@pytest.mark.parametrize("delay", [0.1, 0.2])
def test_log_decorator_execution_time(delay: float) -> None:
    """
    Tests the log decorator's ability to accurately log the execution time of a function.
    This verifies that the decorator appends execution time information to the log.

    Args:
        delay (float): Simulated function execution delay to test timing accuracy.
    """

    with patch('vulcan_logger.decorator.Logger') as mock_logger:
        decorated = log(_slow_function)
        decorated(delay)
        last_call_args = mock_logger.return_value.debug.call_args_list[-1][0][0]
        assert "milliseconds" in last_call_args


def test_log_decorator_basic() -> None:
    """
    Tests the basic functionality of the log decorator to ensure it logs function calls,
    returns, and execution times correctly and returns the expected function results.
    """

    with patch('vulcan_logger.decorator.Logger') as mock_logger:
        decorated = log(_sample_function)
        result = decorated(1, y=3)
        assert result == 4
        assert mock_logger.return_value.debug.call_count == 3


def test_log_decorator_condition_false() -> None:
    """
    Tests the log decorator when the logging condition is set to False.
    Ensures that no logging occurs when the condition evaluates to False but the function
    still executes and returns correctly.
    """

    with patch('vulcan_logger.decorator.Logger') as mock_logger:
        decorated = log(_sample_function, condition=False)
        result = decorated(1, y=3)
        assert result == 4
        mock_logger.return_value.debug.assert_not_called()


def test_log_decorator_log_level() -> None:
    """
    Tests the log decorator's ability to log at a specified level.
    This test ensures that the decorator respects the 'level' parameter and logs at the correct severity.
    """

    with patch('vulcan_logger.decorator.Logger') as mock_logger:
        decorated = log(_sample_function, level="INFO")
        decorated(1, 2)
        assert mock_logger.return_value.info.call_count == 3


def test_retry_success() -> None:
    """
    Verifies that the retry decorator retries the correct number of times and then successfully returns
    the result of the function when it finally succeeds.
    """

    attempts = [0]
    decorated = retry(_failing_function, retries=2, delay=0.1)
    result = decorated(attempts=attempts, max_attempts=2)
    assert result == "Success"
    assert attempts[0] == 2


def test_retry_fail() -> None:
    """
    Ensures that the retry decorator properly raises the last encountered exception after all retries are exhausted.
    """

    attempts = [0]
    decorated = retry(_failing_function, retries=1, delay=0.1)
    with pytest.raises(ValueError):
        decorated(attempts=attempts, max_attempts=3)
    assert attempts[0] == 2


@pytest.mark.parametrize("attempts_list, max_attempts", [([0], 2), ([0], 3)])
def test_retry_logging(attempts_list, max_attempts) -> None:
    """
    Tests that logging occurs as expected during retries and at failure.
    """

    with patch('vulcan_logger.decorator.Logger') as mock_logger:
        decorated = retry(
            _failing_function,
            retries=max_attempts - 1, delay=0.1
        )
        try:
            decorated(attempts=attempts_list, max_attempts=max_attempts)
        except ValueError:
            pass
        expected_warning_calls = max_attempts - 1
        assert mock_logger.return_value.warning.call_count == expected_warning_calls
        assert mock_logger.return_value.error.called == (
            attempts_list[0] == max_attempts)


def test_to_json_decorator():
    """
    Test the to_json decorator to ensure it correctly serializes the return value of a function to a JSON string using
    a custom encoder. The function will return a dictionary which should be serialized into a JSON string.
    """

    @to_json
    def sample_function():
        return {"name": "Alice", "age": 30, "time": datetime(2020, 5, 17)}

    result = sample_function()
    expected_json = json.dumps(
        {"name": "Alice", "age": 30, "time": "2020-05-17T00:00:00"}, cls=Encoder)

    assert result == expected_json, "The JSON output from the decorated function did not match the expected JSON string."

    # Also ensure that it raises no error when trying to serialize more complex data types
    @to_json
    def complex_data_function():
        return {"date": datetime.now(), "data": [1, 2, 3]}

    try:
        json_result = complex_data_function()
        # this will confirm json_result is a valid JSON string
        json.loads(json_result)
        assert True, "Serialization of complex data types was successful."
    except Exception as e:
        assert False, f"Serialization failed with error: {e}"
