"""A simple wrapper around contextlib.suppress"""

import asyncio
import contextlib
from functools import wraps


__version__ = "0.2.0"


def suppress(*exceptions):
    def wrap(func):
        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def inner(*args, **kwargs):
                with contextlib.suppress(exceptions):
                    return await func(*args, **kwargs)
        else:
            @wraps(func)
            def inner(*args, **kwargs):
                with contextlib.suppress(exceptions):
                    return func(*args, **kwargs)
        return inner
    return wrap


# for backward compatibility
async_suppress = suppress
