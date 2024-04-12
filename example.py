# # example.py
import os
import time

from vulcan_utils.cache import Cache
from vulcan_utils.decorator import Decorator
from vulcan_utils.logger import Logger
from vulcan_utils.formatter import Formatter

os.environ["VULCAN_LOG_LEVEL"] = "DEBUG"  # Global log level filter
os.environ["VULCAN_LOG_PATH"] = "logs"  # Path for log files
os.environ["VULCAN_LOG_NAME"] = "example"  # Log file name

logger = Logger(__name__)


@Decorator.log
def baseline_function(x, y):
    """A simple function to demonstrate baseline logging."""
    return x / y


@Decorator.log(level="WARNING")
def level_function(x, y):
    """A function to demonstrate specific level logging."""
    return x + y


@Decorator.log(condition=True)
def condition_function(x, y):
    """A function to demonstrate conditional logging."""
    return x + y


@Decorator.retry(retries=3, delay=1)
def retry_function(x, y):
    """A function that retries upon failure, demonstrated with division."""
    return x / y


@Decorator.to_json
def json_function(data):
    """A function that returns its result in JSON format."""
    return {"data": data}


# Reduced interval for demonstration
@Decorator.rate_limit(limit=3, interval=5)
def rate_limited_function():
    """A function that is rate limited."""
    return "This function is rate-limited."


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
result = baseline_function(10, 2)
result = level_function(10, 5)
result = condition_function(3, 6)
json_result = json_function({"hello": "world"})
logger.info(f"JSON Output: {json_result}")
try:
    result = retry_function(10, 0)
except ZeroDivisionError as e:
    logger.error(f"Caught an exception as expected: {e}")

# Demonstrating rate limiting behavior
for i in range(6):
    response = rate_limited_function()
    if response:
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
