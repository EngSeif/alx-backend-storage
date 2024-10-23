#!/usr/bin/env python3
"""
Main file
"""
import redis

Cache = __import__('exercise').Cache

cache = Cache()

TEST_CASES = {
    b"foo": None,              # No transformation needed
    123: int,                  # Convert bytes to int
    "bar": lambda d: d.decode("utf-8")  # Convert bytes to string (UTF-8)
}

# Store the data in cache and retrieve it with the appropriate conversion
for value, fn in TEST_CASES.items():
    key = cache.store(value)
    print(f"Stored key: {key}, retrieved value: {cache.get(key, fn)}")
