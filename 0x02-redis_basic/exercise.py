#!/usr/bin/env python3
"""
*Redis basic
"""

import redis
import uuid
from typing import Union


class Cache:
    def __init__(self) -> None:
        """Initialize Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the data in Redis with a random key and return the key.
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
