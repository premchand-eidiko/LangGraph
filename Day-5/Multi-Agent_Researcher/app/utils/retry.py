import time
from typing import Callable, Any

from app.utils.logger import logger


def retry_call(
    func: Callable,
    *args,
    attempts: int = 3,
    delay: float = 2,
    retry_exceptions: tuple[type[Exception], ...] = (
        Exception,
    ),
    **kwargs,
) -> Any:

    last_exception = None

    for attempt in range(1, attempts + 1):

        try:

            return func(
                *args,
                **kwargs,
            )

        except retry_exceptions as exc:

            last_exception = exc

            logger.warning(
                "Retryable operation failed | "
                "attempt=%d/%d | error=%s",
                attempt,
                attempts,
                exc,
            )

            if attempt == attempts:
                break

            time.sleep(delay)

    raise last_exception