from unittest.mock import patch
import pytest
from medusa_logger.decorator import log


def sample_function(x, y=2):
    return x + y


def slow_function(delay):
    import time
    time.sleep(delay)
    return delay


@pytest.mark.parametrize("delay", [0.1, 0.2])
def test_log_decorator_execution_time(delay):
    with patch('medusa_logger.decorator.Logger') as mock_logger:
        decorated = log(slow_function)
        decorated(delay)
        last_call_args = mock_logger.return_value.debug.call_args_list[-1][0][0]
        assert "milliseconds" in last_call_args


def test_log_decorator_basic():
    with patch('medusa_logger.decorator.Logger') as mock_logger:
        decorated = log(sample_function)
        result = decorated(1, y=3)
        assert result == 4
        assert mock_logger.return_value.debug.call_count == 3


def test_log_decorator_condition_false():
    with patch('medusa_logger.decorator.Logger') as mock_logger:
        decorated = log(sample_function, condition=False)
        result = decorated(1, y=3)

        assert result == 4
        mock_logger.return_value.debug.assert_not_called()


def test_log_decorator_log_level():
    with patch('medusa_logger.decorator.Logger') as mock_logger:
        decorated = log(sample_function, level="INFO")
        decorated(1, 2)
        assert mock_logger.return_value.info.call_count == 3
