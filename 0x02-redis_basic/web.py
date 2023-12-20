#!/usr/bin/env python3
"""an expiring web cache and tracker
"""

from functools import wraps
import redis
import requests
from typing import Callable


""" redis instance """
redis_history = redis.Redis()


def fetch_data(method: Callable) -> Callable:
    """Fetches the output from cached data
    """

    @wraps(method)
    def cacher(url) -> str:
        """Caches the output
        """
        redis_history.incr(f'count:{url}')
        res = redis_history.get(f'result:{url}')
        if res:
            return res.decode('utf-8')
        res = method(url)
        redis_history.set(f'count:{url}', 0)
        redis_history.setex(f'result:{url}', 10, res}
        return res

    return cacher


@fetch_data
def get_page(url: str) -> str:
    """Uses requests module to obtain the HTML content of a particular URL
    and returns it
    @param (url): <str>

    Return: <str>
    """
    return requests.get(url).text
