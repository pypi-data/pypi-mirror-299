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
from typing import List, Any, Optional, Union

class ArmHashMap:
    """
    Hash table implementation using ctypes for separate chaining and optimized for ARM architecture.
    """

    def __init__(self, initial_capacity: Optional[int] = 16) -> None:
        """Initializes the hash table with a given initial capacity."""
        self.capacity = ctypes.c_int(initial_capacity)
        self.size = ctypes.c_int(0)
        self.buckets = (ctypes.py_object * initial_capacity)()  # Массив списков
        for i in range(initial_capacity):
            self.buckets[i] = []

    def _hash(self, key: Any) -> Optional[int]:
        """Computes the hash value for a given key."""
        return hash(key) % self.capacity.value

    def put(self, key: Any, value: Any) -> None:
        """Inserts or updates the key-value pair in the hash table."""
        hashed_key = self._hash(key)
        bucket = self.buckets[hashed_key]

        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.size.value += 1

        if self.size.value / self.capacity.value > 0.7:
            self._resize()

    def get(self, key: Any) -> Union[Optional[Any], None]:
        """Retrieves the value associated with the given key."""
        hashed_key = self._hash(key)
        bucket = self.buckets[hashed_key]
        for k, v in bucket:
            if k == key:
                return v
        return None

    def remove(self, key: Any) -> Optional[bool]:
        """Removes the key-value pair associated with the given key."""
        hashed_key = self._hash(key)
        bucket = self.buckets[hashed_key]

        for i in range(len(bucket)):
            if bucket[i][0] == key:
                del bucket[i]
                self.size.value -= 1
                return True
        return False

    def _resize(self) -> None:
        """Resizes the hash table when the load factor exceeds 0.7."""
        new_capacity = self.capacity.value * 2
        new_buckets = (ctypes.py_object * new_capacity)()

        for i in range(new_capacity):
            new_buckets[i] = []

        for i in range(self.capacity.value):
            for k, v in self.buckets[i]:
                hashed_key = hash(k) % new_capacity
                new_buckets[hashed_key].append((k, v))

        self.buckets = new_buckets
        self.capacity.value = new_capacity

    def __len__(self) -> Optional[int]:
        """Returns the number of key-value pairs in the hash table."""
        return self.size.value

    def __str__(self) -> Optional[str]:
        """Returns a string representation of the hash table."""
        return str({k: v for bucket in self.buckets for k, v in bucket})

    def keys(self) -> Optional[List[Any]]:
        """Returns a list of all keys in the hash table."""
        return [k for bucket in self.buckets for k, v in bucket]

    def values(self) -> Optional[List[Any]]:
        """Returns a list of all values in the hash table."""
        return [v for bucket in self.buckets for k, v in bucket]

    def items(self) -> Optional[List[Any]]:
        """Returns a list of all key-value pairs in the hash table."""
        return [(k, v) for bucket in self.buckets for k, v in bucket]

    def clear(self) -> None:
        """Clears the hash table, resetting it to its initial state."""
        self.capacity = ctypes.c_int(16)
        self.size = ctypes.c_int(0)
        self.buckets = (ctypes.py_object * self.capacity.value)()
        for i in range(self.capacity.value):
            self.buckets[i] = []

    def contains_key(self, key: Any) -> Optional[bool]:
        """Checks if the given key exists in the hash table."""
        hashed_key = self._hash(key)
        bucket = self.buckets[hashed_key]
        for k, v in bucket:
            if k == key:
                return True
        return False
