from unittest.mock import patch, Mock
import os
import pytest
from medusa_logger.logger import Logger

# Helper function to simulate logging calls within a specific file for _stack_trace


def simulate_logging_call(file_name, line_no, func, message):
    with patch('inspect.stack') as mock_stack:
        mock_frame = Mock()
        mock_frame.filename = file_name
        mock_frame.lineno = line_no
        mock_stack.return_value = [None, mock_frame]
        func(message)


def test_logger_initialization():
    with patch('medusa_logger.logger.coloredlogs.install') as mock_install:
        Logger('test_logger', 'INFO')
        mock_install.assert_called_once()


@pytest.mark.parametrize("method_name", ['debug', 'info', 'warning', 'critical', 'error'])
def test_logging_methods(method_name):
    logger = Logger('test_logger')
    with patch.object(logger.logger, method_name) as mock_log_method:
        simulate_logging_call("test_file.py", 123, getattr(
            logger, method_name), "Test message")
        mock_log_method.assert_called_once()
        assert "test_file.py" in mock_log_method.call_args[1]['extra']['caller_filename']
        assert mock_log_method.call_args[1]['extra']['caller_lineno'] == 123


def test_log_level_from_env():
    os.environ['MD_LOG_LEVEL'] = 'WARNING'
    with patch('medusa_logger.logger.coloredlogs.install') as mock_install:
        Logger('test_logger')
        mock_install.assert_called_once()
        called_args, called_kwargs = mock_install.call_args
        assert 'WARNING' == called_kwargs['level']
