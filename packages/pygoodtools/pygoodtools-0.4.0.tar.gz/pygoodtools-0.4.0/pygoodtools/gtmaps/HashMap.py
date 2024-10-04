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

"""
HashMap is a hash table implementation with separate chaining for collision resolution.

Attributes:
    capacity (Optional[int]): The number of buckets in the hash table.
    size (Optional[int]): The number of key-value pairs in the hash table.
    buckets (Optional[List[List]]): The list of buckets, each bucket is a list of key-value pairs.

Methods:
    __init__(initial_capacity: Optional[int] = 16) -> void:
        Initializes the hash table with a given initial capacity.
    
    _hash(key) -> Optional[int]:
        Computes the hash value for a given key.
    
    put(key: Any, value: Any) -> void:
        Inserts or updates the key-value pair in the hash table.
    
    get(key: Any) -> Union[Optional[int], None]:
        Retrieves the value associated with the given key.
    
    remove(key: Any) -> Optional[bool]:
        Removes the key-value pair associated with the given key.
    
    _resize() -> void:
        Resizes the hash table when the load factor exceeds 0.7.
    
    __len__() -> Optional[int]:
        Returns the number of key-value pairs in the hash table.
    
    __str__() -> Optional[str]:
        Returns a string representation of the hash table.
    
    keys() -> Optional[List]:
        Returns a list of all keys in the hash table.
    
    values() -> Optional[List]:
        Returns a list of all values in the hash table.
    
    items() -> Optional[List]:
        Returns a list of all key-value pairs in the hash table.
    
    clear() -> void:
        Clears the hash table, resetting it to its initial state.
    
    contains_key(key) -> Optional[bool]:
        Checks if the given key exists in the hash table.
"""
from typing import (
    Any,
    final,
    Optional, 
    Tuple, 
    Union,
    List
)
from pygoodtools.gttypes import void
from pygoodtools.metaclasses import HashMapMeta


__all__=[
    'HashMap'
]

@final
class HashMap(metaclass=HashMapMeta):
    def __init__(self, initial_capacity: Optional[int] = 16) -> void:
        self.capacity:  Optional[int]            = initial_capacity
        self.size:      Optional[int]            = 0
        self.buckets:   Optional[List[List]]     = [[] for _ in range(self.capacity)]

    def _hash(self, key) -> Optional[int]:
        return hash(key) % self.capacity

    def put(self, key: Any, value: Any) -> void:
        hashed_key = self._hash(key)
        bucket = self.buckets[hashed_key]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.size += 1
        if self.size / self.capacity > 0.7:
            self._resize()

    def get(self, key: Any) -> Union[Optional[int], None]:
        hashed_key = self._hash(key)
        bucket = self.buckets[hashed_key]
        for k, v in bucket:
            if k == key:
                return v
        return None

    def remove(self, key: Any) -> Optional[bool]:
        hashed_key = self._hash(key)
        bucket = self.buckets[hashed_key]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return True
        return False

    def _resize(self) -> void:
        new_capacity = self.capacity * 2
        new_buckets = [[] for _ in range(new_capacity)]
        for bucket in self.buckets:
            for k, v in bucket:
                hashed_key = hash(k) % new_capacity
                new_buckets[hashed_key].append((k, v))
        self.buckets = new_buckets
        self.capacity = new_capacity

    def __len__(self) -> Optional[int]:
        return self.size

    def __str__(self) -> Optional[str]:
        return str({k: v for bucket in self.buckets for k, v in bucket})

    def keys(self) -> Optional[List]:
        return [k for bucket in self.buckets for k, v in bucket]

    def values(self) -> Optional[List]:
        return [v for bucket in self.buckets for k, v in bucket]

    def items(self) -> Optional[List]:
        return [(k, v) for bucket in self.buckets for k, v in bucket]

    def clear(self) -> void:
        self.capacity = 16
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]

    def contains_key(self, key) -> Optional[bool]:
        hashed_key = self._hash(key)
        bucket = self.buckets[hashed_key]
        for k, v in bucket:
            if k == key:
                return True
        return False