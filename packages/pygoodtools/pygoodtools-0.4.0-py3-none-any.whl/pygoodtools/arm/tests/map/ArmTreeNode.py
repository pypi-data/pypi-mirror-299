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
from typing import List, Optional, Any, Union


class ArmTreeNode(ctypes.Structure):
    _fields_ = [
        ("key", ctypes.py_object),
        ("value", ctypes.py_object),
        ("left", ctypes.POINTER(ctypes.c_void_p)),
        ("right", ctypes.POINTER(ctypes.c_void_p)),
        ("height", ctypes.c_int)
    ]

    def __init__(self, key: Any = None, value: Any = None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class ArmTreeMap:
    """
    TreeMap: Balanced binary search tree (AVL tree) using ctypes for memory management.
    """

    def __init__(self):
        """Initializes an empty TreeMap."""
        self.root = None

    def _height(self, node: Optional[ArmTreeNode]) -> int:
        """Returns the height of the given node."""
        if node is None:
            return 0
        return node.height

    def _update_height(self, node: ArmTreeNode) -> None:
        """Updates the height of the node based on its children."""
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node: ArmTreeNode) -> int:
        """Calculates and returns the balance factor of the node."""
        return self._height(node.left) - self._height(node.right)

    def _rotate_left(self, node: ArmTreeNode) -> ArmTreeNode:
        """Performs a left rotation and returns the new root."""
        right_node = node.right
        node.right = right_node.left
        right_node.left = node
        self._update_height(node)
        self._update_height(right_node)
        return right_node

    def _rotate_right(self, node: ArmTreeNode) -> ArmTreeNode:
        """Performs a right rotation and returns the new root."""
        left_node = node.left
        node.left = left_node.right
        left_node.right = node
        self._update_height(node)
        self._update_height(left_node)
        return left_node

    def _balance(self, node: ArmTreeNode) -> ArmTreeNode:
        """Balances the subtree and returns the new root."""
        self._update_height(node)
        balance_factor = self._balance_factor(node)

        if balance_factor > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if balance_factor < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _insert(self, node: Optional[ArmTreeNode], key: Any, value: Any) -> ArmTreeNode:
        """Inserts a key-value pair into the subtree rooted at the given node."""
        if node is None:
            return ArmTreeNode(key, value)

        if key < node.key:
            if node.left:
                node.left.contents = self._insert(ctypes.cast(node.left, ctypes.POINTER(ArmTreeNode)).contents, key, value)
            else:
                new_node = ArmTreeNode(key, value)
                node.left = ctypes.pointer(ctypes.cast(ctypes.pointer(new_node), ctypes.c_void_p))
        elif key > node.key:
            if node.right:
                node.right.contents = self._insert(ctypes.cast(node.right, ctypes.POINTER(ArmTreeNode)).contents, key, value)
            else:
                new_node = ArmTreeNode(key, value)
                node.right = ctypes.pointer(ctypes.cast(ctypes.pointer(new_node), ctypes.c_void_p))
        else:
            node.value = value
            return node

        self._update_height(node)

        balance = self._get_balance(node)

        if balance > 1 and key < ctypes.cast(node.left, ctypes.POINTER(ArmTreeNode)).contents.key:
            return self._rotate_right(node)

        if balance < -1 and key > ctypes.cast(node.right, ctypes.POINTER(ArmTreeNode)).contents.key:
            return self._rotate_left(node)

        if balance > 1 and key > ctypes.cast(node.left, ctypes.POINTER(ArmTreeNode)).contents.key:
            node.left.contents = self._rotate_left(ctypes.cast(node.left, ctypes.POINTER(ArmTreeNode)).contents)
            return self._rotate_right(node)

        if balance < -1 and key < ctypes.cast(node.right, ctypes.POINTER(ArmTreeNode)).contents.key:
            node.right.contents = self._rotate_right(ctypes.cast(node.right, ctypes.POINTER(ArmTreeNode)).contents)
            return self._rotate_left(node)

        return node

    def insert(self, key: Any, value: Any) -> None:
        """Inserts a key-value pair into the tree."""
        self.root = self._insert(self.root, key, value)

    def _get(self, node: Optional[ArmTreeNode], key: Any) -> Union[None, Any]:
        """Recursively retrieves the value associated with the key."""
        if node is None:
            return None
        if key < node.key:
            return self._get(node.left, key)
        elif key > node.key:
            return self._get(node.right, key)
        return node.value

    def get(self, key: Any) -> Union[None, Any]:
        """Retrieves the value associated with the given key."""
        return self._get(self.root, key)

    def _inorder(self, node: Optional[ArmTreeNode], result: List) -> None:
        """Performs an in-order traversal of the tree."""
        if node is not None:
            self._inorder(node.left, result)
            result.append((node.key, node.value))
            self._inorder(node.right, result)

    def items(self) -> List:
        """Returns a list of key-value pairs in in-order."""
        result = []
        self._inorder(self.root, result)
        return result

    def _search(self, node: Optional[ArmTreeNode], key: Any) -> Optional[ArmTreeNode]:
        """Searches for the node with the given key in the subtree rooted at the given node."""
        if node is None or node.key == key:
            return node

        if key < node.key:
            return self._search(ctypes.cast(node.left, ctypes.POINTER(ArmTreeNode)).contents if node.left else None, key)
        return self._search(ctypes.cast(node.right, ctypes.POINTER(ArmTreeNode)).contents if node.right else None, key)

    def search(self, key: Any) -> Optional[Any]:
        """Searches for the value associated with the given key in the TreeMap."""
        node = self._search(self.root, key)
        if node is None:
            return None
        return node.value