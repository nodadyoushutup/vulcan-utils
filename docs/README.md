<!-- docs/README.md -->
# Vulcan Utils

Vulcan Utils is a Python package designed to enhance the logging capabilities of Python applications. It simplifies the logging process by automatically including critical details like the caller's filename and line number, making it easier to trace the source of log entries. The package supports a range of features including customizable log levels, colored logs, and conditional logging, tailored to improve both the development and debugging processes.

**Requires Python 3.9 or higher**

[View the full technical documentation here](https://vulcan-logger.readthedocs.io/en/latest/)

[View the PyPi project here](https://pypi.org/project/vulcan-utils/)

![Vulcan Utils](https://raw.githubusercontent.com/nodadyoushutup/vulcan-logger/main/docs/img/examples.png)

## Features
- **Caller Information**: Automatically includes the caller's filename and line number in log messages for better traceability.
- **Customizable Log Levels**: Easily configure log levels to control the severity of messages that the logger will process.
- **Colored Logs**: Enhance log readability with colored logs for different log levels.
- **Conditional Logging**: Conditionally log messages based on specific conditions to control verbosity.

## Installation
You can install Vulcan Utils via PIP:

```bash
pip install vulcan-logger
```

## Usage
[View example usage here](https://github.com/nodadyoushutup/vulcan-logger/blob/main/example/example.py)

Below are examples of how to use the Vulcan Utils logging and decoration features.

### Basic Logging
1. Import the Logger class from the `vulcan_utils.logger` module.
2. Initialize a Logger instance with a name and an optional log level. The default log level is INFO.
3. Use the logging methods (debug, info, warning, error, critical) to log messages at various severity levels.

```python
from vulcan_utils.logger import Logger

# Initialize the logger with a custom name and log level
logger = Logger(name='example', level='DEBUG')

# Log messages at different levels
logger.debug("Debug message for detailed diagnostic information")
logger.info("Info message for general information")
logger.warning("Warning message for potential issues")
logger.error("Error message for serious problems")
logger.critical("Critical message for severe conditions")
```

### Function Logging
Vulcan Utils enhances function debugging and monitoring by providing a powerful logging decorator, `log`, which automatically records function calls, their returns, and execution times. This decorator is invaluable for tracing and understanding the flow of execution in complex applications, especially when troubleshooting or monitoring performance.

The log decorator can be configured with different log levels to control the verbosity of the logs generated. In the provided example, the first function logs all calls and returns at the `DEBUG` level, offering detailed insights suitable for in-depth debugging sessions.

Additionally, the decorator supports conditional logging, where logs are generated only if a specified condition is met. This feature is demonstrated in the second function, where logging occurs only if the first argument is greater than the second. This selective logging helps in focusing on significant events, reducing log volume and making important information stand out.

By decorating functions with log, developers can automatically generate detailed logs without manually inserting logging statements, making code cleaner and easier to maintain.

```python
from vulcan_utils.decorator import Decorator

@Decorator.log(level="DEBUG")
def example_log(a, b):
    """Function to demonstrate logging with a decorator."""
    return a + b

@Decorator.log(condition=lambda args, kwargs: args[0] > args[1])
def example_conditional_log(x, y):
    """Function that logs only if the condition is true."""
    return x * y

# Call the decorated functions
sum_result = example_log(1, 2)
product_result = example_conditional_log(5, 3)
```

### Retry
The `retry` decorator allows you to automatically retry executing a function if it raises an exception. The decorator can be customized with the number of retry attempts and the delay between retries. It can also call the function repeatedly indefinitely. This feature is especially useful in scenarios where operations might occasionally fail due to transient issues, such as network connectivity problems. In this example, the function attempts to divide two numbers and will retry up to three times with a one-second pause between attempts if an exception occurs.

```python
from vulcan_utils.decorator import Decorator

@Decorator.retry(retries=3, delay=1)
def example_retry(x, y):
    """A function that retries upon failure, demonstrated with division."""
    return x / y

@Decorator.retry(infinite=True, delay=1)
def example_retry_infinite(x, y):
    """A function that retries upon failure indefinitely, demonstrated with division."""
    return x / y
```

### JSON Serialization
The `to_json` decorator automatically serializes the return value of the function into JSON format using a custom encoder. This decorator simplifies the process of converting Python objects into JSON strings, which is often required in web development and APIs for communicating between the server and client. The decorator will also convert non-standard custom objects to serialized JSON. The example provided demonstrates how to return a Python dictionary as a JSON-formatted string, making it a handy tool for data serialization tasks.

```python
@Decorator.to_json
def example_to_json(data):
    """A function that returns its result in JSON format."""
    return {"data": data}
```

### Rate Limiting
The `rate_limit` decorator is crucial for controlling the rate of operations to manage resource consumption or maintain service availability under high demand. The rate_limit decorator enforces a limit on how many times a function can be called within a specified time interval. In this example, the function can only be invoked three times per minute, which helps prevent excessive usage and ensures fair resource access when dealing with limited or shared resources.

```python
@Decorator.rate_limit(limit=3, interval=60)
def example_rate_limit():
    """A function that is rate limited."""
    return "This function is rate-limited."
```

### Advanced Configuration
Vulcan Utils offers several environment variables to fine-tune logging behavior for your application. You can set these variables before initializing your logger to customize logging output, destination, and file naming.

#### Setting Global Log Level
Control the log level globally across your application by setting the `VULCAN_LOG_LEVEL` environment variable. This determines the minimum level of messages that will be logged. Available levels are `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`.

_bash_
```bash
export VULCAN_LOG_LEVEL="WARNING"
```

_python_
```python
os.environ["VULCAN_LOG_LEVEL"] = "WARNING"
```

#### Setting Log File Path
By default, Vulcan Utils writes logs to the current directory. Set the `VULCAN_LOG_PATH` environment variable to specify a custom directory for log files.

_bash_
```bash
export VULCAN_LOG_PATH="~/logs"
```

_python_
```python
os.environ["VULCAN_LOG_PATH"] = "~/logs"
```

#### Setting Log File Name
The default log file name is `vulcan`. Use the `VULCAN_LOG_NAME` environment variable to specify a different name for the log file. It will automatically use the `.log` extension type and does not need to be included in the name.

_bash_
```bash
export VULCAN_LOG_NAME="example"
```

_python_
```python
os.environ["VULCAN_LOG_NAME"] = "example"
```

### Handling Exceptions
Vulcan Utils makes it easy to log exceptions. Use the logging methods within exception handling blocks to log errors and critical issues.

```python
try:
    # Potentially problematic code
    result = 10 / 0
except ZeroDivisionError as e:
    logger.error(f"Caught an exception: {e}")
```

## Contributing
Contributions to Vulcan Utils are welcome! To contribute, follow these steps:

1. Fork the repository and clone it to your local machine.
2. Install the development dependencies by running `pip install -r requirements.txt`.
3. Make your changes and ensure tests pass by running `pytest`.
4. Submit a pull request with a clear description of your changes and why they are beneficial.

Please adhere to the [code of conduct](https://github.com/jacobfholland/vulcan-logger/blob/main/docs/CODE_OF_CONDUCT.md) when contributing to this project.

## License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/jacobfholland/vulcan-logger/blob/main/LICENSE) file for details.
