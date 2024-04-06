# Medusa Logger

Medusa Logger is a Python package that provides a customizable logging utility with support for automatic inclusion of caller's filename and line number in logs. It aims to simplify logging in Python applications by offering features such as log level configuration, colored logs, and conditional logging.

## Features

- **Caller Information**: Automatically includes the caller's filename and line number in log messages for better traceability.
- **Customizable Log Levels**: Easily configure log levels to control the severity of messages that the logger will process.
- **Colored Logs**: Enhance log readability with colored logs for different log levels.
- **Conditional Logging**: Conditionally log messages based on specific conditions to control verbosity.

## Installation

You can install Medusa Logger via pip:

```bash
pip install medusa-logger
```

## Usage

To use Medusa Logger in your Python project, follow these steps:

1. Import the `Logger` class from `medusa_logger.logger`.
2. Initialize a logger instance with optional parameters such as name and log level.
3. Start logging messages using the available logging methods (`debug`, `info`, `warning`, `error`, `critical`).

Example:

```python
from medusa_logger.logger import Logger

# Initialize logger
logger = Logger(name='my_logger', level='DEBUG')

# Log messages
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
```

For more advanced usage, Medusa Logger also provides a logging decorator for functions, which logs function calls, returns, and execution time.

## Contributing

Contributions to Medusa Logger are welcome! To contribute, follow these steps:

1. Fork the repository and clone it to your local machine.
2. Install the development dependencies by running `pip install -r requirements.txt`.
3. Make your changes and ensure tests pass by running `pytest`.
4. Submit a pull request with a clear description of your changes and why they are beneficial.

Please adhere to the [code of conduct](CODE_OF_CONDUCT.md) when contributing to this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
