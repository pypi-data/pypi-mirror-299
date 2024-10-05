# COPYRIGHT (c) 2024 Massonskyi
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


import ctypes
import functools

__all__ = ['arm_lru_cache', 'ArmLRUCache']
__version__ = '0.1.0'
__description__ = 'Кэширует результаты функции с ограничением на размер кэша.'

from typing import Any

class ArmLRUCache(ctypes.Structure):
    _fields_ = [("cache", ctypes.py_object), ("order", ctypes.py_object), ("maxsize", ctypes.c_int)]

    def __init__(self, maxsize=128, *args: Any, **kw: Any):
        super().__init__(*args, **kw)
        self.cache = {}
        self.order = []
        self.maxsize = maxsize

    def get(self, key):
        if key in self.cache:
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return None

    def put(self, key, value):
        if key in self.cache:
            self.order.remove(key)
        self.cache[key] = value
        self.order.append(key)
        if len(self.order) > self.maxsize:
            oldest_key = self.order.pop(0)
            del self.cache[oldest_key]

def arm_lru_cache(maxsize=128):
    """
    Decorator to implement a Least Recently Used (LRU) cache.
    Args:
        maxsize (int, optional): The maximum size of the cache. Defaults to 128.
    Returns:
        function: A decorator that wraps a function with LRU caching.
    The LRU cache stores the results of function calls and reuses them when the same inputs occur again, 
    up to a maximum number of cached items specified by `maxsize`. When the cache exceeds `maxsize`, 
    the least recently used items are discarded to make room for new ones.
    Example:
        @lru_cache(maxsize=100)
        def expensive_function(x, y):
            # Expensive computation here
        # The first call will compute the result
        result1 = expensive_function(1, 2)
        # The second call with the same arguments will return the cached result
        result2 = expensive_function(1, 2)
    """
    
    def decorator_lru_cache(func):
        cache = ArmLRUCache(maxsize)

        @functools.wraps(func)
        def wrapper_lru_cache(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            cached_result = cache.get(key)
            if cached_result is not None:
                return cached_result
            result = func(*args, **kwargs)
            cache.put(key, result)
            return result

        return wrapper_lru_cache

    return decorator_lru_cache