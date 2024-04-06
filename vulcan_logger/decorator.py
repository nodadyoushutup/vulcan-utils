# medusa_logger/decorator.py
import json
import time
from functools import wraps
from typing import Any, Callable, Optional, TypeVar, Union

from .encoder import Encoder
from .logger import Logger

# TypeVar for decorator type preservation
F = TypeVar('F', bound=Callable[..., Any])


def _call_message(func: Callable[..., Any], *args: Any, **kwargs: Any) -> str:
    """
    Constructs a log message string for function calls, including function name,
    positional arguments, and keyword arguments.

    Args:
        func: The function being called.
        *args: Positional arguments passed to the function.
        **kwargs: Keyword arguments passed to the function.

    Returns:
        A formatted log message string.
    """

    log_message_parts = [f"{func.__name__} call:"]
    if args:
        log_message_parts.append(f"args:{args}")
    if kwargs:
        log_message_parts.append(f"kwargs:{kwargs}")
    return ' '.join(log_message_parts)


def _return_message(func: Callable[..., Any], result: Any) -> str:
    """
    Constructs a log message string for function returns, including function name and the serialized return value.

    Args:
        func: The function that returned a value.
        result: The return value of the function.

    Returns:
        A formatted log message string with the serialized return value.
    """

    json_result = json.dumps(result, cls=Encoder, ensure_ascii=False)
    return f"{func.__name__} return: {json_result} {type(result)}"


def _log_func(logger: Logger, level: str) -> Callable[[str], None]:
    """
    Retrieves the appropriate logging function based on the specified log level.

    Args:
        logger: An instance of Logger.
        level: A string representing the logging level.

    Returns:
        A logging function from the Logger instance.
    """

    levels = {
        "DEBUG": logger.debug,
        "INFO": logger.info,
        "WARNING": logger.warning,
        "CRITICAL": logger.critical,
        "ERROR": logger.error,
    }
    return levels.get(level.upper(), logger.debug)


def log(_func: Optional[F] = None, *, condition: bool = True, level: str = "DEBUG") -> Union[Callable[[F], F], F]:
    """
    A decorator that logs the call and return of functions, including execution time. Optionally, logging can be
    conditioned on a boolean expression.

    Args:
        _func: The function to be decorated. Defaults to None, allowing other parameters to be specified first.
        condition: A boolean flag to determine if logging should occur. Defaults to True.
        level: A string indicating the logging level. Defaults to "DEBUG".

    Returns:
        The decorated function, with logging capabilities added.
    """

    def decorator_log(func: F):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            if condition:
                start_time = time.time()
                logger = Logger(func.__module__)
                log_func = _log_func(logger, level)
                log_func(_call_message(func, *args, **kwargs))
                result = func(*args, **kwargs)
                log_func(_return_message(func, result))
                end_time = time.time()
                execution_time_ms = round(
                    (end_time - start_time) * 1000,
                    ndigits=4
                )
                log_func(
                    f"{func.__name__} executed: {execution_time_ms} milliseconds")
            else:
                result = func(*args, **kwargs)
            return result
        return wrapper
    if _func is None:
        return decorator_log
    else:
        return decorator_log(_func)
