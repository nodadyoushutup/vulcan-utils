"""
Example

This module provides a collection of functions and utilities for demonstration purposes. 
It includes functions for logging at different levels, retrying operations upon failure, 
rate-limiting function calls, working with environment variables, formatting durations, 
and using caching mechanisms.

Functions:
- baseline_function: A simple function demonstrating baseline logging.
- level_function: A function demonstrating logging at a specific level.
- condition_function: A function demonstrating conditional logging.
- retry_function: A function that retries upon failure.
- json_function: A function that returns its result in JSON format.
- rate_limited_function: A function that is rate-limited.
- env_function_exists: A function that only executes if a specific environment variable is set.
- env_function_debug: A function that only executes if a specific environment variable is set to 
    'DEBUG'.
- env_function_critical: A function that only executes if a specific environment variable is set 
    to 'CRITICAL'.

Logging Levels:
- DEBUG: Detailed information, typically of interest only when diagnosing problems.
- INFO: Confirmation that things are working as expected.
- WARNING: Indication that something unexpected happened or indicative of some problem in the near 
    future.
- ERROR: Due to a more serious problem, the software has not been able to perform some function.
- CRITICAL: A serious error, indicating that the program itself may be unable to continue running.
"""

import os
import time

from vulcan_utils.cache import Cache
from vulcan_utils.decorator import env, log, rate_limit, retry, to_json
from vulcan_utils.formatter import Formatter
from vulcan_utils.logger import Logger

os.environ["VULCAN_LOG_LEVEL"] = "DEBUG"
os.environ["VULCAN_LOG_PATH"] = "logs"
os.environ["VULCAN_LOG_NAME"] = "example"

logger = Logger(__name__)


@log
def baseline_function(x, y):
    """A simple function to demonstrate baseline logging."""
    return x / y


@log(level="WARNING")
def level_function(x, y):
    """A function to demonstrate specific level logging."""
    return x + y


@log(condition=True)
def condition_function(x, y):
    """A function to demonstrate conditional logging."""
    return x + y


@retry(retries=3, delay=1)
def retry_function(x, y):
    """A function that retries upon failure, demonstrated with division."""
    return x / y


@to_json
def json_function(data):
    """A function that returns its result in JSON format."""
    return {"data": data}


@rate_limit(limit=3, interval=5)
def rate_limited_function():
    """A function that is rate limited."""
    return "This function is rate-limited."


@env(variable="VULCAN_LOG_LEVEL")
def env_function_exists():
    """A function that only executes if the 'VULCAN_LOG_LEVEL' environment variable is set."""
    return "Environment-specific function executed successfully."


@env(variable="VULCAN_LOG_LEVEL", value="DEBUG")
def env_function_debug():
    """A function that only executes if the 'VULCAN_LOG_LEVEL' environment variable is set to 
        'DEBUG'."""
    return "Environment-specific function executed successfully."


@env(variable="VULCAN_LOG_LEVEL", value="CRITICAL")
def env_function_critical():
    """A function that only executes if the 'VULCAN_LOG_LEVEL' environment variable is set to 
        'CRITICAL'."""
    return "Environment-specific function executed successfully."


# Logging manual messages
logger.error("Test logging on the error level")
logger.critical("Test logging on the critical level")
logger.warning("Test logging on the warning level")
logger.info("Test logging on the info level")
logger.debug("Test logging on the debug level")

# Using Formatter for duration formatting
formatter = Formatter()
formatted_duration = formatter.duration(
    1234567890,
    format_type=str,
    delimiter=" "
)
logger.info(f"Formatted duration: {formatted_duration}")

# Calling functions with decorators
baseline_function(10, 2)
level_function(10, 5)
condition_function(3, 6)
json_function({"hello": "world"})
env_function_exists()
env_function_debug()
env_function_critical()
try:
    retry_function(1, 0)
except ZeroDivisionError as e:
    logger.error(f"Caught an exception as expected: {e}")
for i in range(6):
    RESPONSE = rate_limited_function()
    if RESPONSE:
        logger.info(f"Call {i + 1}: Success")
    time.sleep(1)


# Using Caching
# Must install `redis-tools` and `redis-server` first
cache = Cache()
cache.set("user:1", {"name": "John", "age": 30}, expire=3600)
user = cache.get("user:1")
logger.info(f"Cache get: {user}")
cache.delete("user:1")
cache.clear()
