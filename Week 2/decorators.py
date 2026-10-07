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


def retry(
    times: int = 3, delay: float = 0.1
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Retry a function up to `times` attempts, waiting `delay` seconds between tries."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: object, **kwargs: object) -> T:
            last_exc: Exception | None = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except (
                    Exception
                ) as exc:  # noqa: BLE001 - intentional: retry on any failure
                    last_exc = exc
                    logger.warning(
                        "Attempt %d/%d for %s failed: %s",
                        attempt,
                        times,
                        func.__name__,
                        exc,
                    )
                    if attempt < times:
                        time.sleep(delay)
            assert last_exc is not None
            raise last_exc

        return wrapper

    return decorator