# Vulcan Logger
Vulcan Logger is a Python package that provides a customizable logging utility with support for automatic inclusion of caller's filename and line number in logs. It aims to simplify logging in Python applications by offering features such as log level configuration, colored logs, and conditional logging.

[View the full documentation here](https://vulcan-logger.readthedocs.io/en/latest/)

![Vulcan Logger](https://raw.githubusercontent.com/nodadyoushutup/vulcan-logger/main/docs/img/examples.png)

## Features
- **Caller Information**: Automatically includes the caller's filename and line number in log messages for better traceability.
- **Customizable Log Levels**: Easily configure log levels to control the severity of messages that the logger will process.
- **Colored Logs**: Enhance log readability with colored logs for different log levels.
- **Conditional Logging**: Conditionally log messages based on specific conditions to control verbosity.

## Installation
You can install Vulcan Logger via pip:

```bash
pip install vulcan-logger
```

## Usage
[Please check out example usage here](https://github.com/nodadyoushutup/vulcan-logger/blob/main/example/example.py)

### Basic Logging
1. Import the Logger class from the vulcan_logger.logger module.
2. Initialize a Logger instance with a name and an optional log level. The default log level is INFO.
3. Use the logging methods (debug, info, warning, error, critical) to log messages at various severity levels.
```python
from vulcan_logger.logger import Logger

# Initialize the logger with a custom name and log level
logger = Logger(name='application_log', level='DEBUG')

# Log messages at different levels
logger.debug("Debug message for detailed diagnostic information")
logger.info("Info message for general information")
logger.warning("Warning message for potential issues")
logger.error("Error message for serious problems")
logger.critical("Critical message for severe conditions")
```

### Function Logging with Decorators
Vulcan Logger provides a logging decorator that can be applied to functions to automatically log calls, returns, and execution times. To use this feature:

1. Import the log decorator from the vulcan_logger.decorator module.
2. Apply the @log decorator to any function. You can optionally specify a log level or a condition for logging.
```python
from vulcan_logger.decorator import log

@log(level="DEBUG")
def compute_sum(a, b):
    """Function to demonstrate logging with a decorator."""
    return a + b

@log(condition=lambda args, kwargs: args[0] > args[1])
def conditional_log_example(x, y):
    """Function that logs only if the condition is true."""
    return x * y

# Call the decorated functions
sum_result = compute_sum(1, 2)
product_result = conditional_log_example(5, 3)
```

### Advanced Configuration
Vulcan Logger offers several environment variables to fine-tune logging behavior for your application. You can set these variables before initializing your logger to customize logging output, destination, and file naming.

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
By default, Vulcan Logger writes logs to the current directory. Set the `VULCAN_LOG_PATH` environment variable to specify a custom directory for log files.

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
Vulcan Logger makes it easy to log exceptions. Use the logging methods within exception handling blocks to log errors and critical issues.

```python
try:
    # Potentially problematic code
    result = 10 / 0
except ZeroDivisionError as e:
    logger.error(f"Caught an exception: {e}")
```

## Contributing
Contributions to Vulcan Logger are welcome! To contribute, follow these steps:

1. Fork the repository and clone it to your local machine.
2. Install the development dependencies by running `pip install -r requirements.txt`.
3. Make your changes and ensure tests pass by running `pytest`.
4. Submit a pull request with a clear description of your changes and why they are beneficial.

Please adhere to the [code of conduct](https://github.com/jacobfholland/vulcan-logger/blob/main/docs/CODE_OF_CONDUCT.md) when contributing to this project.

## License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/jacobfholland/vulcan-logger/blob/main/LICENSE) file for details.
