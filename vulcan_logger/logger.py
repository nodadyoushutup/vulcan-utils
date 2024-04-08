# medusa_logger/logger.py
import inspect
import logging
import os
import sys
from types import TracebackType
from typing import Callable, Optional

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
    A customizable logger class designed to enhance logging functionality by automatically
    including the caller's filename and line number in log messages. This feature provides
    detailed contextual information, facilitating easier debugging and log analysis. The logger
    supports configuring different log levels, colored console output, and optional file logging.

    Attributes:
        _logger (logging.Logger): The underlying logger instance from the standard logging library.
        level (str): The log level as a string, determining the severity of messages to be processed.
        file_name (str): The name of the file where logs will be written, if file logging is enabled.
        path (Optional[str]): The directory path for the log file. If not specified, file logging may 
            be disabled or use a default path.
    """

    def __init__(
        self,
        name: str = __name__,
        level: Optional[str] = None,
        file_name: Optional[str] = None,
        path: Optional[str] = None
    ) -> None:
        """
        Initializes a Logger instance with a specified name, logging level, filename, and path
        for log file output. This constructor configures the underlying logger instance, sets
        the log level, and prepares file and colored console logging as specified.

        Args:
            name (str): The name of the logger, defaulting to the name of the module in which
                the Logger is instantiated. It is used for identification in log messages.
            level (Optional[str]): The initial logging level as a string (e.g., "DEBUG", "INFO").
                If not specified, defaults to "DEBUG" or a level set by the
                VULCAN_LOG_LEVEL environment variable.
            file_name (Optional[str]): The name of the log file. If not specified, it defaults to a
                value determined by the VULCAN_LOG_NAME environment variable
                or a default filename if the variable is not set.
            path (Optional[str]): The path where the log file will be stored. If not provided,
                the path is determined by the VULCAN_LOG_PATH environment variable
                or defaults to None, potentially disabling file logging.

        """

        self._logger = logging.getLogger(name)
        self.level = self._level(level)
        self.file_name = self._file_name(file_name)
        self.path = self._path(path)
        self._setup()

    def _path(self, path: Optional[str]) -> Optional[str]:
        """
        Determines the path for logging output. This path can be explicitly provided, set through
        an environment variable, or defaults to None if neither is specified.

        Args:
            path (Optional[str]): An explicit path for the log output.

        Returns:
            Optional[str]: The determined path as a string, or None if no path is determined.
        """

        # TODO: Validate path before returning it.
        env_log_path = os.environ.get("VULCAN_LOG_PATH")
        if path:
            return path
        elif env_log_path:
            return env_log_path
        return None

    def _level(self, level: Optional[str]) -> str:
        """
        Determines the effective log level for the logger instance, based on direct input or environment variables.

        Args:
            level (Optional[str]): A specified log level as a string.

        Returns:
            str: The determined log level as a string.
        """

        # TODO: Validate level before returning it.
        env_log_level = os.environ.get("VULCAN_LOG_LEVEL")
        if level:
            return level.upper()
        elif env_log_level:
            return env_log_level
        return "DEBUG"

    def _file_name(self, name: Optional[str]) -> str:
        """
        Constructs the filename for the log file based on an environment variable or a default name.

        Returns:
            str: The filename for the log file.
        """

        env_log_file_name = os.environ.get("VULCAN_LOG_NAME")
        if name:
            return name
        elif env_log_file_name:
            return f"{env_log_file_name}.log"
        return "vulcan.log"

    def _install_coloredlogs(self) -> None:
        """
        Installs and configures coloredlogs for the logger instance, setting the logging level,
        format, and date format for console output. If an error occurs during installation,
        logs the error using the logger's error method.
        """

        try:
            coloredlogs.install(
                level=os.environ.get("VULCAN_LOG_LEVEL", self.level).upper(),
                logger=self._logger,
                fmt=LOG_FORMAT,
                datefmt=DATE_FORMAT
            )
        except Exception as e:
            self.error(f"Error installing coloredlogs: {e}")

    def _file_handler(self) -> None:
        """
        Configures a file handler for logging, setting the log file path, level, and format.
        """

        try:
            if self.path:
                path = os.path.join(self.path, self.file_name)
                file_handler = logging.FileHandler(path)
                file_handler.setLevel(self.level.upper())
                formatter = logging.Formatter(
                    fmt=LOG_FORMAT,
                    datefmt=DATE_FORMAT
                )
                file_handler.setFormatter(formatter)
                self._logger.addHandler(file_handler)
        except Exception as e:
            self.error(f"Error creating log file handler: {e}")

    def _setup(self) -> None:
        """
        Sets up the logging format, date format, installs colored logs, and configures file logging if VULCAN_LOG_PATH is set.
        """

        self._install_coloredlogs()
        if self.path:
            try:
                self._file_handler()
            except Exception as e:
                self.error(
                    f"Error setting up file handler for logger: {e}")

    def _stack_trace(self) -> dict:
        """
        Generates a stack trace to identify the caller's filename and line number, excluding specified files and modules.

        Returns:
            dict: A dictionary with keys 'caller_filename' and 'caller_lineno', representing the file and line number of the log call origin.
        """

        stack = inspect.stack()
        caller_info = {"caller_filename": "Unknown", "caller_lineno": 0}
        for frame_info in stack[1:]:
            if not frame_info.filename.endswith(EXCLUDE):
                caller_info['caller_filename'] = os.path.basename(
                    frame_info.filename
                )
                caller_info['caller_lineno'] = frame_info.lineno
                break
        return caller_info

    def _exc_info(self) -> tuple[Optional[type], Optional[BaseException], Optional[TracebackType]]:
        """
        Checks if there is an exception being handled in the current context and returns a tuple of exception information.

        Returns:
            tuple[Optional[type], Optional[BaseException], Optional[TracebackType]]: A tuple containing exception type, exception instance, and traceback information.
        """
        exc_info = sys.exc_info()
        if exc_info:
            return exc_info[0] is not None
        return False

    def _base(self, func: Callable[[str, dict, bool], None], message: str) -> None:
        """
        A base logging function that enriches log messages with caller details and conditional exception information.

        Args:
            func (Callable[[str, dict, bool], None]): A logging function (e.g., self._logger.debug) to be invoked with enriched logging information.
            message (str): The log message.
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

        self._base(self._logger.debug, message)

    def info(self, message: str) -> None:
        """
        Logs an info message.

        Args:
            message: The message to log.
        """

        self._base(self._logger.info, message)

    def warning(self, message: str) -> None:
        """
        Logs a warning message.

        Args:
            message: The message to log.
        """

        self._base(self._logger.warning, message)

    def critical(self, message: str) -> None:
        """
        Logs a critical message.

        Args:
            message: The message to log.
        """

        self._base(self._logger.critical, message)

    def error(self, message: str) -> None:
        """
        Logs a error message.

        Args:
            message: The message to log.
        """

        self._base(self._logger.error, message)
