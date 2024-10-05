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
from typing import List, Optional, Any, final
@final
class ArmMap:
    """
    A dictionary-like data structure using ctypes for optimized performance, especially for ARM architecture.
    """

    def __init__(self, initial_capacity: Optional[int] = 16) -> None:
        """Initializes the hash table with a given initial capacity."""
        self.capacity = ctypes.c_int(initial_capacity)
        self.size = ctypes.c_int(0)
        self._map = (ctypes.py_object * initial_capacity)()  # Массив значений
        self._keys = (ctypes.py_object * initial_capacity)()  # Массив ключей

    def _resize(self) -> None:
        """Resize the internal storage if capacity is exceeded."""
        new_capacity = self.capacity.value * 2
        new_map = (ctypes.py_object * new_capacity)()
        new_keys = (ctypes.py_object * new_capacity)()

        # Копируем старые значения в новый массив
        for i in range(self.size.value):
            new_map[i] = self._map[i]
            new_keys[i] = self._keys[i]

        self._map = new_map
        self._keys = new_keys
        self.capacity.value = new_capacity

    def put(self, key: Any, value: Any) -> None:
        """Add a key-value pair to the map."""
        if self.size.value == self.capacity.value:
            self._resize()

        # Сохраняем ключ и значение
        self._keys[self.size.value] = ctypes.py_object(key)
        self._map[self.size.value] = ctypes.py_object(value)
        self.size.value += 1
        
    def remove(self, key: Any) -> bool:
        """Remove a key-value pair from the map by key."""
        for i in range(self.size.value):
            if self._keys[i] == key:
                # Удаляем ключ и значение, смещая оставшиеся элементы
                for j in range(i, self.size.value - 1):
                    self._keys[j] = self._keys[j + 1]
                    self._map[j] = self._map[j + 1]
                self.size.value -= 1
                return True
        return False

    def get(self, key: Any) -> Any:
        """Retrieve a value by key from the map."""
        for i in range(self.size.value):
            if self._keys[i] == key:
                return self._map[i]
        return None

    def get_p(self, key: Any) -> Optional[ctypes.POINTER(ctypes.py_object)]: # type: ignore
        """Retrieve a pointer to the value by key from the map."""
        for i in range(self.size.value):
            if self._keys[i] == key:
                return ctypes.pointer(self._map[i])
        return None

    def contains(self, key: Any) -> Optional[bool]:
        """Check if a key is in the map."""
        for i in range(self.size.value):
            if self._keys[i] == key:
                return True
        return False

    def size(self) -> Optional[int]:
        """Return the number of key-value pairs in the map."""
        return self.size.value

    def clear(self) -> None:
        """Remove all key-value pairs from the map."""
        self.size.value = 0

    def keys(self) -> Optional[List[Any]]:
        """Return a list of all keys in the map."""
        return [self._keys[i] for i in range(self.size.value)]

    def values(self) -> Optional[List[Any]]:
        """Return a list of all values in the map."""
        return [self._map[i] for i in range(self.size.value)]

    def items(self) -> Optional[List[Any]]:
        """Return a list of all key-value pairs in the map."""
        return [(self._keys[i], self._map[i]) for i in range(self.size.value)]

    def update(self, key: Any, value: Any) -> None:
        """Update the value for a given key in the map."""
        for i in range(self.size.value):
            if self._keys[i] == key:
                self._map[i] = ctypes.py_object(value)
                return
        raise KeyError(f"Key {key} not found in map.")

    def merge(self, other_map: 'ArmMap') -> None:
        """Merge another map into this map."""
        for i in range(other_map.size()):
            self.add(other_map._keys[i], other_map._map[i])

    def get_key(self, value: Any) -> Any:
        """Retrieve a key by value from the map."""
        for i in range(self.size.value):
            if self._map[i] == value:
                return self._keys[i]
        return None

    def is_empty(self) -> Optional[bool]:
        """Check if the map is empty."""
        return self.size.value == 0
    
    def __len__(self) -> int:
        """Return the number of key-value pairs in the map."""
        return self.size.value
    
    def __str__(self) -> Optional[str]:
        """Return a string representation of the map."""
        return str({self._keys[i]: self._map[i] for i in range(self.size.value)})
