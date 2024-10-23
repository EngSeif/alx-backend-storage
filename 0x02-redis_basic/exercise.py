#!/usr/bin/env python3
"""
*Redis basic
"""

import redis
import uuid
from typing import Union


class Cache:
    """
    *Cache Class To Store Cache Data
    *into Redis Server
    """
    def __init__(self) -> None:
        """
        *Initialize Redis client and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, float, int, bytes]) -> str:
        """
        *Store the data in Redis with a random key and return the key.
        !Args:
            *data: The data to store in Redis
            *(can be str, bytes, int, or float).
        !Returns:
            *str: The key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
