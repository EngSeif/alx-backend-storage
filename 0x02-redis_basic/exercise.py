#!/usr/bin/env python3
"""
*Redis basic
"""

import redis
import uuid
from typing import Union


class Cache():
    """
    *Cache Class To Store Cache Data
    *into Redis Server
    """
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, float, int, bytes]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
