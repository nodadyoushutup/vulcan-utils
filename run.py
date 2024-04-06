# run.py
from medusa_logger.decorator import log
from medusa_logger.logger import Logger


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


logger = Logger(__name__)
logger.critical("Test logging on the critical level")
logger.warning("Test logging on the warning level")
logger.info("Test logging on the info level")
logger.debug("Test logging on the info level")

try:
    result = baseline_function(10, 2)
    result = baseline_function(10, 0)
except ZeroDivisionError as e:
    logger.error(f"Caught an exception as expected: {e}")


result = level_function(10, 2)
result = condition_function(3, 6)
