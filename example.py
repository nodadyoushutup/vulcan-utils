# example/example.py
import os

from vulcan_logger.logger import Logger
from vulcan_logger.decorator import log


os.environ["VULCAN_LOG_LEVEL"] = "DEBUG"  # Global log level filter

# Functions defined with a log decorator. Level or Condition may be
# passed as arguments on the decorator, or omitted.


@log
def baseline_function(x, y):
    """A simple function to demonstrate baseline logging."""
    return x / y


@log(level="WARNING")
def level_function(x, y):
    """A simple function to demonstrate specific level logging."""
    return x + y


@log(condition=True)
def condition_function(x, y):
    """A simple function to demonstrate condition logging."""
    return x + y


# Individual log statements
logger = Logger(__name__)
logger.error("Test logging on the error level")
# logger.critical("Test logging on the critical level")
# logger.warning("Test logging on the warning level")
# logger.info("Test logging on the info level")
# logger.debug("Test logging on the info level")

# # Calling functions that have @log decorator
# result = baseline_function(10, 2)
# result = level_function(x="foo", y="bar")
# result = condition_function(3, 6)

# try:
#     result = baseline_function(10, 0)
# except ZeroDivisionError as e:
#     logger.error(f"Caught an exception as expected: {e}")
