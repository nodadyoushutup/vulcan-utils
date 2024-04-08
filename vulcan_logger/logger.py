# medusa_logger/logger.py
import inspect
import logging
import os
import sys
from typing import Callable

import coloredlogs

EXCLUDE = (
    'decorator.py',
    'logger.py',
    'logging/__init__.py',
    '<frozen importlib._bootstrap>'
)

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s - (%(caller_filename)s:%(caller_lineno)d)"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


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

    def _install_coloredlogs(self):
        try:
            coloredlogs.install(
                level=os.environ.get("VULCAN_LOG_LEVEL", self.level).upper(),
                logger=self.logger,
                fmt=LOG_FORMAT,
                datefmt=DATE_FORMAT
            )
        except Exception as e:
            self.error(f"Error installing coloredlogs: {e}")

    def _file_name(self):
        return f"{os.environ.get('VULCAN_LOG_NAME', 'vulcan')}.log"

    def _make_dir(self, log_path):
        try:
            if not os.path.isdir(log_path):
                os.makedirs(log_path, exist_ok=True)
        except Exception as e:
            self.error(f"Error creating the log directory: {e}")

    def _file_handler(self, log_path):
        try:

            log_path = os.path.join(log_path, self._file_name())
            file_handler = logging.FileHandler(log_path)
            file_handler.setLevel(os.environ.get(
                "VULCAN_LOG_LEVEL", self.level).upper()
            )
            formatter = logging.Formatter(
                fmt=LOG_FORMAT,
                datefmt=DATE_FORMAT
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        except Exception as e:
            self.error(f"Error creating log file handler: {e}")

    def _setup(self) -> None:
        """
        Sets up the logging format, date format, installs colored logs, and configures file logging if VULCAN_LOG_PATH is set.
        """

        self._install_coloredlogs()
        log_path = os.environ.get(
            "VULCAN_LOG_PATH",
            os.path.abspath(os.path.curdir)
        )
        if log_path:
            try:
                self._make_dir(log_path)
                self._file_handler(log_path)
            except Exception as e:
                self.error(
                    f"Error setting up file handler for logger: {e}")

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

    def _exc_info(self) -> bool:
        """
        Determines if there is currently an exception being handled. This method checks if the
        sys.exc_info() method returns any exception information.

        Returns:
            bool: True if there is an exception being handled, False otherwise.
        """

        exc_info = sys.exc_info()
        if exc_info:
            return exc_info[0] is not None
        return False

    def _base(self, func: Callable[[str, dict, bool], None], message: str) -> None:
        """
        Base function for logging a message, automatically including the caller's
        filename and line number, and conditionally including exception information
        based on the current execution context.

        This method checks if there is an exception being currently handled and
        includes this information in the log if present.

        Args:
            func: The logging function to be called (debug, info, warning, etc.).
                This function must accept a message, extra information (in a dict),
                and a boolean indicating whether to log exception info.
            message: The log message to be recorded.
        """

        caller_info = self._stack_trace()
        exc_info = self._exc_info()
        func(message, extra=caller_info, exc_info=exc_info)

    def debug(self, message: str) -> None:
        """
        Logs a debug message.

        Args:
            message: The message to log.
        """

        self._base(self.logger.debug, message)

    def info(self, message: str) -> None:
        """
        Logs an info message.

        Args:
            message: The message to log.
        """

        self._base(self.logger.info, message)

    def warning(self, message: str) -> None:
        """
        Logs a warning message.

        Args:
            message: The message to log.
        """

        self._base(self.logger.warning, message)

    def critical(self, message: str) -> None:
        """
        Logs a critical message.

        Args:
            message: The message to log.
        """

        self._base(self.logger.critical, message)

    def error(self, message: str) -> None:
        """
        Logs a error message.

        Args:
            message: The message to log.
        """

        self._base(self.logger.error, message)
