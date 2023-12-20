#!/usr/bin/env python3
"""an expiring web cache and tracker
"""
import redis
import requests
from functools import wraps
from typing import Callable


redis_history = redis.Redis()
"""Redis instance
"""


def data_cacher(method: Callable) -> Callable:
    """Fetches the output from cached data
    """
    @wraps(method)
    def invoker(url) -> str:
        """caches the output.
        """
        redis_history.incr(f'count:{url}')
        result = redis_history.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_history.set(f'count:{url}', 0)
        redis_history.setex(f'result:{url}', 10, result)
        return result

    return invoker


@data_cacher
def get_page(url: str) -> str:
    """Uses requests module to obtain the HTML content of a particular URL
    and returns it
    @param (url): <str>

    Return: <str>
    """
    return requests.get(url).text
