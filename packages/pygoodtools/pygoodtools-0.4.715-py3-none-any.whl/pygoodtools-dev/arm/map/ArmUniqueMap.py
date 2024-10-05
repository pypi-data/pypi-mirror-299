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
from typing import Any, List, final
class UniqueMapNode(ctypes.Structure):
    _fields_ = [
        ("key", ctypes.py_object),
        ("value", ctypes.py_object)
    ]

@final
class ArmUniqueMap:
    """
    Unique map class using ctypes for memory efficiency.
    Maintains a collection of unique elements in the order of their insertion.
    """

    def __init__(self) -> None:
        """
        Initialize the UniqueMap instance with an empty data structure and order list.
        """
        self._data: dict = {}
        self._order: List = []

    @property
    def collection(self) -> set:
        """
        Returns the collection of unique items stored in the map.
        """
        return set(self._data.keys())

    @property
    def order(self) -> List:
        """
        Returns the insertion order of the items in the map.
        """
        return self._order

    @collection.setter
    def collection(self, collection: set) -> None:
        """
        Set a collection of unique items to the map.
        """
        if not isinstance(collection, set) or not collection:
            raise ValueError('collection must be a non-empty set')

        if self._data:
            raise ValueError('collection cannot overwrite an existing map')

        self._data = {item: None for item in collection}
        self._order = list(self._data.keys())

    @order.setter
    def order(self, order: List) -> None:
        """
        Set the insertion order of the items in the map.
        """
        if not isinstance(order, list) or not order:
            raise ValueError('order must be a non-empty list')

        if self._data:
            raise ValueError('order cannot overwrite an existing map')

        self._order = order.copy()
        self._data = {item: None for item in self._order}

    def add(self, item: Any) -> None:
        """
        Add an item to the map if it does not already exist.
        If already present, do nothing.
        """
        if item not in self._data:
            self._data[item] = None
            self._order.append(item)

    def remove(self, key: Any) -> None:
        """
        Remove an item from the map if it exists. If not present, do nothing.
        """
        if key in self._data:
            del self._data[key]
            self._order.remove(key)

    def __contains__(self, key: Any) -> bool:
        """
        Check if a given key exists in the map.
        """
        return key in self._data

    def __len__(self) -> int:
        """
        Return the number of unique items in the map.
        """
        return len(self._data)

    def __iter__(self) -> Any:
        """
        Iterate over the items in the map in their insertion order.
        """
        return iter(self._order)

    def __repr__(self) -> str:
        """
        Return the representation of the map.
        """
        return f'{self.__class__.__name__}({list(self._data.keys())})'

    def __str__(self) -> str:
        """
        Return the string representation of the map.
        """
        return str(list(self._data.keys()))

    def __getitem__(self, key: Any) -> Any:
        """
        Get an item by its key.
        """
        return self._data[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set an item by its key.
        """
        self._data[key] = value

    def __delitem__(self, key: Any) -> None:
        """
        Delete an item by its key.
        """
        self.remove(key)
