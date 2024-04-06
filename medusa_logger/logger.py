# medusa_logger/logger.py
import inspect
import logging
import os
from typing import Callable

import coloredlogs

EXCLUDE = (
    'decorator.py',
    'logger.py',
    'logging/__init__.py',
    '<frozen importlib._bootstrap>'
)


class Logger:
    """
    A customizable logger class that supports automatic inclusion of caller's filename and line 
    number in logs. The logger can be configured with different log levels and conditionally.

    Attributes:
        logger (logging.Logger): The underlying logger instance from the standard logging library.
        level (str): The log level as a string. This determines the severity of messages that the logger will process.

    Args:
        name (str, optional): The name of the logger. Defaults to the module's name.
        level (str, optional): The logging level as a string. Defaults to "DEBUG".
    """

    def __init__(self, name: str = __name__, level: str = "DEBUG") -> None:
        """
        Initializes a new Logger instance with a specified name and log level.

        Args:
            name: The name of the logger. Defaults to the module's name.
            level: The logging level as a string. Defaults to "DEBUG".
        """
        self.logger = logging.getLogger(name)
        self.level = level.upper()
        self._setup()

    def _setup(self) -> None:
        """
        Sets up the logging format, date format, and installs colored logs.
        """

        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s - (%(caller_filename)s:%(caller_lineno)d)"
        date_format = "%Y-%m-%d %H:%M:%S"
        coloredlogs.install(
            level=os.environ.get("MD_LOG_LEVEL", self.level).upper(),
            logger=self.logger,
            fmt=log_format,
            datefmt=date_format
        )

    def _stack_trace(self) -> dict:
        """
        Generates a stack trace to find the caller's filename and line number,
        ignoring specific files and modules.

        Returns:
            A dictionary containing the caller's filename and line number.
        """

        stack = inspect.stack()
        caller_info = {'caller_filename': 'Unknown', 'caller_lineno': 0}
        for frame_info in stack[1:]:
            if not frame_info.filename.endswith(EXCLUDE):
                caller_info['caller_filename'] = os.path.basename(
                    frame_info.filename)
                caller_info['caller_lineno'] = frame_info.lineno
                break
        return caller_info

    def _base(self, func: Callable[[str, bool], None], message: str, exc_info: bool) -> None:
        """
        Base function for logging a message, automatically including the caller's
        filename and line number.

        Args:
            func: The logging function to be called (debug, info, warning, etc.).
            message: The log message.
            exc_info: Whether to include exception information in the log.
        """

        caller_info = self._stack_trace()
        func(message, extra=caller_info, exc_info=exc_info)

    def debug(self, message: str) -> None:
        """
        Logs a debug message.

        Args:
            message: The message to log.
        """

        self._base(self.logger.debug, message, exc_info=False)

    def info(self, message: str) -> None:
        """
        Logs an info message.

        Args:
            message: The message to log.
        """

        self._base(self.logger.info, message, exc_info=False)

    def warning(self, message: str) -> None:
        """
        Logs a warning message.

        Args:
            message: The message to log.
        """

        self._base(self.logger.warning, message, exc_info=False)

    def critical(self, message: str) -> None:
        """
        Logs a critical message.

        Args:
            message: The message to log.
        """

        self._base(self.logger.critical, message, exc_info=False)

    def error(self, message: str) -> None:
        """
        Logs a error message.

        Args:
            message: The message to log.
        """

        self._base(self.logger.error, message, exc_info=True)
