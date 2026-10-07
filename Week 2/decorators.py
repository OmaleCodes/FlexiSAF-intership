"""Reusable decorators: a timing decorator and a retry decorator."""

import functools
import logging
import time
from collections.abc import Callable
from typing import TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


def timed(func: Callable[..., T]) -> Callable[..., T]:
    """Log how long a function takes to run, without changing its return value."""

    @functools.wraps(func)
    def wrapper(*args: object, **kwargs: object) -> T:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info("%s took %.6f seconds", func.__name__, elapsed)
        return result

    return wrapper


