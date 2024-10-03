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
Map.py
This module defines the `Map` class, which provides a dictionary-like data structure with additional methods for managing key-value pairs.
Classes:
    Map: A final class that provides methods to add, remove, retrieve, and manipulate key-value pairs in a map.
Methods:
    __init__() -> void:
        Initialize an empty map.
    add(key: Any, value: Any) -> void:
        Add a key-value pair to the map.
    remove(key: Any) -> void:
        Remove a key-value pair from the map by key.
    get(key: Any) -> Any:
        Retrieve a value by key from the map.
    get_p(key: Any) -> Optional[ptr]:
        Retrieve a ptr value by key from the map.
    contains(key: Any) -> Optional[bool]:
        Check if a key is in the map.
    size() -> Optional[int]:
        Return the number of key-value pairs in the map.
    clear() -> void:
        Remove all key-value pairs from the map.
    keys() -> Optional[List]:
        Return a list of all keys in the map.
    values() -> Optional[List]:
        Return a list of all values in the map.
    items() -> Optional[List]:
        Return a list of all key-value pairs in the map.
    update(key: Any, value: Any) -> void:
        Update the value for a given key in the map.
    merge(other_map: 'Map') -> void:
        Merge another map into this map.
    get_key(value: Any) -> Any:
        Retrieve a key by value from the map.
    is_empty() -> Optional[bool]:
        Check if the map is empty.
    __str__() -> Optional[str]:
        Return a string representation of the map.
"""
from typing import (
    List,
    final,
    Any,
    Optional
)

from pygoodtools.metaclasses import MapMeta
from pygoodtools.gttypes import void, ptr

__all__ = ["Map"]

@final
class Map(metaclass=MapMeta):
    def __init__(self) -> void:
        self._map: dict = {}

    def add(self, key: Any, value: Any) -> void:
        """Add a key-value pair to the map."""
        self._map[key] = value

    def remove(self, key: Any) -> void:
        """Remove a key-value pair from the map by key."""
        if key in self._map:
            del self._map[key]
        else:
            raise KeyError(f"Key {key} not found in map.")

    def get(self, key: Any) -> Any:
        """Retrieve a value by key from the map."""
        return self._map.get(key, None)
    
    def get_p(self, key: Any) -> Optional[ptr]:
        """Retrieve a ptr value by key from the map."""
        return ptr(obj=self._map.get(key, None))
    
    def contains(self, key: Any) -> Optional[bool]:
        """Check if a key is in the map."""
        return key in self._map

    def size(self) -> Optional[int]:
        """Return the number of key-value pairs in the map."""
        return len(self._map)

    def clear(self) -> void:
        """Remove all key-value pairs from the map."""
        self._map.clear()

    def keys(self) -> Optional[List]:
        """Return a list of all keys in the map."""
        return list(self._map.keys())

    def values(self)-> Optional[List]:
        """Return a list of all values in the map."""
        return list(self._map.values())

    def items(self)-> Optional[List]:
        """Return a list of all key-value pairs in the map."""
        return list(self._map.items())

    def update(self, key: Any, value: Any) -> void:
        """Update the value for a given key in the map."""
        if key in self._map:
            self._map[key] = value
        else:
            raise KeyError(f"Key {key} not found in map.")

    def merge(self, other_map: 'Map') -> void:
        """Merge another map into this map."""
        if isinstance(other_map, Map):
            self._map.update(other_map._map)
        else:
            raise TypeError("Argument must be of type Map.")

    def get_key(self, value: Any) -> Any:
        """Retrieve a key by value from the map."""
        for k, v in self._map.items():
            if v == value:
                return k
        return None

    def is_empty(self) -> Optional[bool]:
        """Check if the map is empty."""
        return len(self._map) == 0

    def __str__(self) -> Optional[str]:
        """Return a string representation of the map."""
        return str(self._map)