from unittest.mock import patch, Mock
import os
import pytest
from vulcan_logger.logger import Logger


def _simulate_logging_call(file_name: str, line_no: int, func: callable, message: str) -> None:
    """
    Simulates a logging call with specified file name and line number information.

    This helper function is designed to mock the behavior of a logging call while
    allowing the specification of the file name and line number from which the log
    would appear to have been called.

    Args:
        file_name: The name of the file to appear as the source of the log message.
        line_no: The line number to appear as the source of the log message.
        func: The logging function to be called.
        message: The log message to be passed to the logging function.
    """

    with patch('inspect.stack') as mock_stack:
        mock_frame = Mock()
        mock_frame.filename = file_name
        mock_frame.lineno = line_no
        mock_stack.return_value = [None, mock_frame]
        func(message)


def test_logger_initialization() -> None:
    """
    Tests the initialization process of the Logger class.

    Verifies that the `coloredlogs.install` method is called exactly once during
    the initialization of a Logger instance, ensuring that the logger setup process
    is executed properly.
    """

    with patch('vulcan_logger.logger.coloredlogs.install') as mock_install:
        Logger('test_logger', 'INFO')
        mock_install.assert_called_once()


@pytest.mark.parametrize("method_name", ['debug'])
def test_debug(method_name: str) -> None:
    """
    Tests the debug logging method of the Logger class.

    Args:
        method_name: The name of the Logger method to test.
    """

    logger = Logger('test_logger')
    with patch.object(logger._logger, method_name) as mock_log_method:
        _simulate_logging_call("test_file.py", 123, getattr(
            logger, method_name), "Test message")
        mock_log_method.assert_called_once()
        assert "test_file.py" in mock_log_method.call_args[1]['extra']['caller_filename']
        assert mock_log_method.call_args[1]['extra']['caller_lineno'] == 123


@pytest.mark.parametrize("method_name", ['info'])
def test_info(method_name: str) -> None:
    """
    Tests the info logging method of the Logger class.

    Args:
        method_name: The name of the Logger method to test.
    """

    logger = Logger('test_logger')
    with patch.object(logger._logger, method_name) as mock_log_method:
        _simulate_logging_call("test_file.py", 123, getattr(
            logger, method_name), "Test message")
        mock_log_method.assert_called_once()
        assert "test_file.py" in mock_log_method.call_args[1]['extra']['caller_filename']
        assert mock_log_method.call_args[1]['extra']['caller_lineno'] == 123


@pytest.mark.parametrize("method_name", ['warning'])
def test_warning(method_name: str) -> None:
    """
    Tests the warning logging method of the Logger class.

    Args:
        method_name: The name of the Logger method to test.
    """

    logger = Logger('test_logger')
    with patch.object(logger._logger, method_name) as mock_log_method:
        _simulate_logging_call("test_file.py", 123, getattr(
            logger, method_name), "Test message")
        mock_log_method.assert_called_once()
        assert "test_file.py" in mock_log_method.call_args[1]['extra']['caller_filename']
        assert mock_log_method.call_args[1]['extra']['caller_lineno'] == 123


@pytest.mark.parametrize("method_name", ['critical'])
def test_critical(method_name: str) -> None:
    """
    Tests the critical logging method of the Logger class.

    Args:
        method_name: The name of the Logger method to test.
    """

    logger = Logger('test_logger')
    with patch.object(logger._logger, method_name) as mock_log_method:
        _simulate_logging_call("test_file.py", 123, getattr(
            logger, method_name), "Test message")
        mock_log_method.assert_called_once()
        assert "test_file.py" in mock_log_method.call_args[1]['extra']['caller_filename']
        assert mock_log_method.call_args[1]['extra']['caller_lineno'] == 123


@pytest.mark.parametrize("method_name", ['error'])
def test_error(method_name: str) -> None:
    """
    Tests the errorlogging method of the Logger class.

    Args:
        method_name: The name of the Logger method to test.
    """

    logger = Logger('test_logger')
    with patch.object(logger._logger, method_name) as mock_log_method:
        _simulate_logging_call("test_file.py", 123, getattr(
            logger, method_name), "Test message")
        mock_log_method.assert_called_once()
        assert "test_file.py" in mock_log_method.call_args[1]['extra']['caller_filename']
        assert mock_log_method.call_args[1]['extra']['caller_lineno'] == 123


def test_log_level_from_env() -> None:
    """
    Tests that the Logger respects the log level specified by an environment variable.

    Sets the 'VULCAN_LOG_LEVEL' environment variable to 'WARNING' and verifies that the
    Logger instance initializes with the log level correctly set to 'WARNING', as indicated
    by the arguments passed to `coloredlogs.install`.
    """

    os.environ['VULCAN_LOG_LEVEL'] = 'WARNING'
    with patch('vulcan_logger.logger.coloredlogs.install') as mock_install:
        Logger('test_logger')
        mock_install.assert_called_once()
        called_args, called_kwargs = mock_install.call_args
        assert 'WARNING' == called_kwargs['level']
