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
from typing import Any, Dict, final

class KeyValuePair(ctypes.Structure):
    _fields_ = [
        ("key", ctypes.py_object),
        ("value", ctypes.py_object)
    ]


@final
class ArmUnorderedMap:
    """
    UnorderedMap is a simple implementation of a hash map (dictionary) that allows
    insertion, deletion, and lookup of key-value pairs. It supports typical dictionary
    operations such as getting, setting, deleting items, and checking for the existence
    of keys. Additionally, it provides methods to retrieve all keys, values, and items,
    as well as to clear and update the map.
    """

    def __init__(self) -> None:
        """
        Initialize an empty UnorderedMap.
        """
        self._data: Dict[Any, Any] = {}

    def insert(self, key: Any, value: Any) -> None:
        """
        Insert a key-value pair into the map.
        """
        self._data[key] = value

    def remove(self, key: Any) -> None:
        """
        Remove the key-value pair associated with the given key from the map.
        Raises a KeyError if the key is not found.
        """
        if key in self._data:
            del self._data[key]
        else:
            raise KeyError(f"Key '{key}' not found in UnorderedMap.")

    def find(self, key: Any) -> Any:
        """
        Return the value associated with the given key, or None if the key is not found.
        """
        return self._data.get(key, None)

    def __getitem__(self, key: Any) -> Any:
        """
        Return the value associated with the given key.
        Raises a KeyError if the key is not found.
        """
        if key in self._data:
            return self._data[key]
        else:
            raise KeyError(f"Key '{key}' not found in UnorderedMap.")

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set the value for the given key in the map.
        """
        self._data[key] = value

    def __delitem__(self, key: Any) -> None:
        """
        Delete the key-value pair associated with the given key.
        Raises a KeyError if the key is not found.
        """
        if key in self._data:
            del self._data[key]
        else:
            raise KeyError(f"Key '{key}' not found in UnorderedMap.")

    def __contains__(self, key: Any) -> bool:
        """
        Check if the given key exists in the map.
        """
        return key in self._data

    def __len__(self) -> int:
        """
        Return the number of key-value pairs in the map.
        """
        return len(self._data)

    def __iter__(self):
        """
        Return an iterator over the keys of the map.
        """
        return iter(self._data)

    def items(self):
        """
        Return a view object that displays a list of the map's key-value tuple pairs.
        """
        return self._data.items()

    def keys(self):
        """
        Return a view object that displays a list of the map's keys.
        """
        return self._data.keys()

    def values(self):
        """
        Return a view object that displays a list of the map's values.
        """
        return self._data.values()

    def clear(self) -> None:
        """
        Remove all items from the map.
        """
        self._data.clear()

    def update(self, other: Any) -> None:
        """
        Update the map with the key-value pairs from another UnorderedMap or dictionary,
        overwriting existing keys. Raises a TypeError if the argument is not of type
        UnorderedMap or dict.
        """
        if isinstance(other, ArmUnorderedMap):
            self._data.update(other._data)
        elif isinstance(other, dict):
            self._data.update(other)
        else:
            raise TypeError("Argument must be of type UnorderedMap or dict.")
