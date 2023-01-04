import sys
import time
import typing as t
from datetime import datetime, timedelta
from functools import wraps

from async_lru import alru_cache
from loguru import logger


def exc_info():
    """Get current exception information
    :return: Return current exception information: (type, value).
    """
    type_, value, _ = sys.exc_info()
    return type_, value


def latency(func: t.Callable):
    """Decorator to calculate endpoint latency. Print latency and response logs.
    :param: func: A callaable function

    :return: A callaable function
    """

    @wraps(func)
    async def wrapped_func(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)

        if result:
            message = f"[+] {result}"
            logger.log("RESPONSE", message)

        logger.log("LATENCY", f"[+] {round(time.time() - start_time, 10)} s")
        return result

    return wrapped_func


def cache(seconds: int, maxsize: int = 128):
    """Decorator to applay cache with expiration time, allows to return the response of the function
    if it was previously called. It can save time when an expensive or I/O bound function is periodically called
    with the same arguments.

    :param: seconds: expiration time in seconds
    :param: maxsize: maximum size to cache.

    :return: function response
    """

    def wrapper_cache(func):
        func = alru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        async def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime

            return await func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache
