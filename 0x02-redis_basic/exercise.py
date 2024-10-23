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
    """ Display the history of calls for the given method. """
    r = redis.Redis()
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"
    
    # Retrieve inputs and outputs from Redis
    inputs = r.lrange(input_key, 0, -1)
    outputs = r.lrange(output_key, 0, -1)

    # Print the number of calls
    print(f"{method.__qualname__} was called {len(inputs)} times:")

    # Loop over inputs and outputs together using zip
    for input_data, output_data in zip(inputs, outputs):
        # Decode bytes to string for readability
        input_tuple = eval(input_data.decode('utf-8'))  # Convert bytes back to tuple
        output_value = output_data.decode('utf-8')  # Decode output
        print(f"{method.__qualname__}(*{input_tuple}) -> {output_value}")


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
