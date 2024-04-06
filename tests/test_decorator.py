from unittest.mock import patch
import pytest
from vulcan_logger.decorator import log


def _sample_function(x, y=2):
    return x + y


def _slow_function(delay):
    import time
    time.sleep(delay)
    return delay


@pytest.mark.parametrize("delay", [0.1, 0.2])
def test_log_decorator_execution_time(delay: float) -> None:
    """
    Tests the log decorator's ability to log the execution time of a function.

    Args:
        delay (float): A float representing the delay (in seconds) to simulate in the function.
    """

    with patch('vulcan_logger.decorator.Logger') as mock_logger:
        decorated = log(_slow_function)
        decorated(delay)
        last_call_args = mock_logger.return_value.debug.call_args_list[-1][0][0]
        assert "milliseconds" in last_call_args


def test_log_decorator_basic() -> None:
    """
    Tests the basic functionality of the log decorator.

    Verifies that a simple decorated function returns the expected result
    and that the logger's debug method is called three times (for the function call,
    return, and execution time logging).
    """

    with patch('vulcan_logger.decorator.Logger') as mock_logger:
        decorated = log(_sample_function)
        result = decorated(1, y=3)
        assert result == 4
        assert mock_logger.return_value.debug.call_count == 3


def test_log_decorator_condition_false() -> None:
    """
    Tests the log decorator with the condition set to False.

    Verifies that when the log decorator is applied with a condition that evaluates
    to False, the decorated function executes normally but logging does not occur.
    """

    with patch('vulcan_logger.decorator.Logger') as mock_logger:
        decorated = log(_sample_function, condition=False)
        result = decorated(1, y=3)
        assert result == 4
        mock_logger.return_value.debug.assert_not_called()


def test_log_decorator_log_level() -> None:
    """
    Tests the log decorator's ability to log at a specified log level.

    Checks that when a log level of "INFO" is specified, the decorated
    function's activities are logged using the logger's info method instead of the
    default debug method.
    """

    with patch('vulcan_logger.decorator.Logger') as mock_logger:
        decorated = log(_sample_function, level="INFO")
        decorated(1, 2)
        assert mock_logger.return_value.info.call_count == 3
