#!/usr/bin/env python3
"""A Cache module that sets up a redis environment
"""

from functools import wraps
from typing import Any, Callable, Union
import redis
import uuid


def count_calls(method: Callable) -> Callable:
    """Track how many times methods of the Cache class are called
    Return: <Callable>
    """
    @wraps(method)
    def counter(self, *args, **kwargs) -> Any:
        """Invokes the given method after incrementing its call counter.
        Return: <Any>
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return counter


def call_history(method: Callable) -> Callable:
    """Tracks the call details of a method in a Cache class
    Return: <Callable>
    """
    @wraps(method)
    def tracker(self, *args, **kwargs) -> Any:
        """Returns the method's output after storing it's inputs and outputs
        Return: <Any>
        """
        input_k = f'{method.__qualname__}:inputs'
        output_k = f'{method.__qualname__}:outputs'

        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_k, str(args))

        result = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_k, result)
        return result
    return tracker


def replay(fn: Callable) -> None:
    """Displays the call history of a Cache Class method
    Return: None
    """
    if fn is None or not hasattr(fn, '__self__'):
        return

    history = getattr(fn.__self__, '_redis', None)
    if not isinstance(history, redis.Redis):
        return

    method_name = fn.__qualname__
    input_k = f'{method_name}:inputs'
    output_k = f'{method_name}:outputs'
    method_count = 0

    if history.exists(method_name) != 0:
        method_count = int(history.get(method_name))

    print(f'{method_name} was called {method_count} times:')
    method_inputs = history.lrange(input_k, 0, -1)
    method_outputs = history.lrange(output_k, 0, -1)

    for func_in, func_out in zip(method_inputs, method_outputs):
        print(f'{method_name}(*{func_in}.decode("utf-8")) -> {func_out}')


class Cache():
    """class Implementation
    """

    def __init__(self) -> None:
        """Constructor
        Stores an instance of the Redis client and flush the
        instance using flushdb
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        @param (data): <Union type>
        Return: <str>
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, float]:
        """
        @param (key): <str>
        @param (fn): <Callable> converts the data to desired format

        Return: <Union type> if fn else None
        """
        res = self._redis.get(key)
        return fn(res) if fn else res

    def get_str(self, key: str) -> str:
        """
        @param (key): <str>
        Return: <str>
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> str:
        """
        @param (key): <str>
        Return: <int>
        """
        return self.get(key, lambda x: int(x))
