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
Methods
-------
__init__():
    Initializes an empty UnorderedMap.

insert(key, value):
    Inserts a key-value pair into the map.

remove(key):
    Removes the key-value pair associated with the given key from the map.
    Raises a KeyError if the key is not found.

find(key):
    Returns the value associated with the given key, or None if the key is not found.

__getitem__(key):
    Returns the value associated with the given key.
    Raises a KeyError if the key is not found.

__setitem__(key, value):
    Sets the value for the given key in the map.

__delitem__(key):
    Deletes the key-value pair associated with the given key.
    Raises a KeyError if the key is not found.

__contains__(key):
    Checks if the given key exists in the map.

__len__():
    Returns the number of key-value pairs in the map.

__iter__():
    Returns an iterator over the keys of the map.

items():
    Returns a view object that displays a list of the map's key-value tuple pairs.

keys():
    Returns a view object that displays a list of the map's keys.

values():
    Returns a view object that displays a list of the map's values.

clear():
    Removes all items from the map.

update(other):
    Updates the map with the key-value pairs from another UnorderedMap or dictionary,
    overwriting existing keys. Raises a TypeError if the argument is not of type
    UnorderedMap or dict.
"""

"""
UnorderedMap is a simple implementation of a hash map (dictionary) that allows
insertion, deletion, and lookup of key-value pairs. It supports typical dictionary
operations such as getting, setting, deleting items, and checking for the existence
of keys. Additionally, it provides methods to retrieve all keys, values, and items,
as well as to clear and update the map.
"""
class UnorderedMap:
    def __init__(self):
        self._data = {}

    def insert(self, key, value):
        self._data[key] = value

    def remove(self, key):
        if key in self._data:
            del self._data[key]
        else:
            raise KeyError(f"Key '{key}' not found in UnorderedMap.")

    def find(self, key):
        return self._data.get(key, None)

    def __getitem__(self, key):
        if key in self._data:
            return self._data[key]
        else:
            raise KeyError(f"Key '{key}' not found in UnorderedMap.")

    def __setitem__(self, key, value):
        self._data[key] = value

    def __delitem__(self, key):
        if key in self._data:
            del self._data[key]
        else:
            raise KeyError(f"Key '{key}' not found in UnorderedMap.")

    def __contains__(self, key):
        return key in self._data

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def items(self):
        return self._data.items()

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def clear(self):
        """Remove all items from the map."""
        self._data.clear()

    def update(self, other):
        """Update the map with the key/value pairs from other, overwriting existing keys."""
        if isinstance(other, UnorderedMap):
            self._data.update(other._data)
        elif isinstance(other, dict):
            self._data.update(other)
        else:
            raise TypeError("Argument must be of type UnorderedMap or dict.")