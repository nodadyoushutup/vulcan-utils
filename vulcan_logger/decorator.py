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


def retry(_func: Optional[F] = None, *, retries: int = 3, delay: Union[int, float] = 1) -> Union[Callable[[F], F], F]:
    """
    Decorator to retry a function if it raises an exception. Retries the function a specified number of times with
    a given delay between each attempt. If all attempts fail, the last exception is raised.

    Args:
        _func: The function to be decorated. Defaults to None, allowing other parameters to be specified first.
        retries: The maximum number of retries before giving up and raising the exception.
        delay: The delay between retries in seconds, which can be an integer or a float for partial seconds.

    Returns:
        The decorated function that will retry on exceptions, or raises the last encountered exception if all retries fail.

    Raises:
        Exception: The last exception encountered if the retry attempts exceed the specified limit.
    """

    def decorator_retry(func: F):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal retries
            last_exception = None
            for attempt in range(retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < retries:
                        logger = Logger(func.__module__)
                        left = retries - attempt - 1
                        logger.warning(
                            f"{func.__name__} failed, retrying: {e}, attempts left: {left}"
                        )
                        time.sleep(delay)
                    else:
                        logger.error(
                            f"{func.__name__} retry attemps failed: {e}")
                        break
            raise last_exception
        return wrapper
    if _func is not None:
        return decorator_retry(_func)
    return decorator_retry
