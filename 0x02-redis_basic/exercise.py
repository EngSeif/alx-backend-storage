#!/usr/bin/env python3
"""
Redis basic
"""

from functools import wraps
import redis
import uuid
from typing import Callable, Optional, Union


def count_calls(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        output = method(self, *args)
        self._redis.rpush(output_key, str(output))
        return output
    return wrapper


def replay(method: Callable):
    """
    Prototype: def replay(func: Callable):
    Displays history of calls of a particular function
    """
    r = redis.Redis()
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"
    func_name = method.__qualname__
    inputs = r.lrange(input_key, 0, -1)
    outputs = r.lrange(output_key, 0, -1)
    calls_num = len(inputs)
    times_str = 'times'
    if calls_num == 1:
        times_str = 'time'
    print(f"{method.__qualname__} was called {calls_num} {times_str}:")
    for k, v in zip(inputs, outputs):
        print(f"{func_name}(*{k.decode('utf-8')}) -> {v.decode('utf-8')}")


class Cache:
    def __init__(self) -> None:
        """Initialize Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the data in Redis with a random key and return the key.
        Args:
            data: The data to store in Redis
            (can be str, bytes, int, or float).
        Returns:
            str: The key under which the data is stored.
        """
        # Generate a random key
        key = str(uuid.uuid4())
        # Store the data in Redis using the generated key
        self._redis.set(key, data)
        # Return the key
        return key

    def get(self, key, fn: Optional[Callable] = None) -> Union[
                                                    str, bytes, int, float]:
        """
        Get data from Redis and
        apply the conversion function if provided.
        """
        data = self._redis.get(key)
        if not data:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """Get data as a string."""
        value = self.get(key)
        return value.decode("utf-8")

    def get_int(self, key: int) -> Optional[int]:
        """Get data as a int."""
        return self.get(key, int)
