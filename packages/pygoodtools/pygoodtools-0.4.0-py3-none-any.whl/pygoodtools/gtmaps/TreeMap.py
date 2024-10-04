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
TreeMap and TreeNode classes for implementing a balanced binary search tree (AVL tree).

Classes:
    TreeNode: A node in the TreeMap, containing a key, value, left and right children, and height for balancing.
    TreeMap: A balanced binary search tree (AVL tree) implementation.

TreeNode:
    Attributes:
        key (Optional[Any]): The key of the node.
        value (Optional[Any]): The value associated with the key.
        left (Optional[TreeNode]): The left child node.
        right (Optional[TreeNode]): The right child node.
        height (int): The height of the node for balancing purposes.

TreeMap:
    Attributes:
        root (Optional[TreeNode]): The root node of the tree.

    Methods:
        _height(node: Optional[TreeNode]) -> int:
            Returns the height of the given node.

        _update_height(node: TreeNode) -> void:
            Updates the height of the given node based on its children's heights.

        _balance_factor(node: TreeNode) -> int:
            Returns the balance factor of the given node.

        _rotate_left(node: TreeNode) -> TreeNode:
            Performs a left rotation on the given node and returns the new root of the subtree.

        _rotate_right(node: TreeNode) -> TreeNode:
            Performs a right rotation on the given node and returns the new root of the subtree.

        _balance(node: TreeNode) -> TreeNode:
            Balances the given node and returns the new root of the subtree.

        _put(node: Optional[TreeNode], key: Any, value: Any) -> TreeNode:
            Recursively inserts a key-value pair into the tree and returns the new root of the subtree.

        put(key: Any, value: Any) -> void:
            Inserts a key-value pair into the tree.

        _get(node: Optional[TreeNode], key: Any) -> Union[void, Any]:
            Recursively retrieves the value associated with the given key from the tree.

        get(key: Any) -> Union[void, Any]:
            Retrieves the value associated with the given key from the tree.

        _inorder(node: Optional[TreeNode], result: List) -> void:
            Performs an in-order traversal of the tree and appends key-value pairs to the result list.

        items() -> List:
            Returns a list of all key-value pairs in the tree in in-order.
"""
from typing import List, Optional, Any, Union, final
from pygoodtools.gttypes import void
from dataclasses import dataclass

__all__=[
    'TreeNode',
    'TreeMap'
]

@dataclass
@final
class TreeNode:
    key:    Optional[Any] = None
    value:  Optional[Any] = None
    left:   Optional[Any] = None
    right:  Optional[Any] = None
    height: int = 1  # Add height for balancing

@final
class TreeMap:
    def __init__(self):
        self.root: Optional[TreeNode] = None

    def _height(self, node: Optional[TreeNode]) -> int:
        if node is None:
            return 0
        return node.height

    def _update_height(self, node: TreeNode) -> void:
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node: TreeNode) -> int:
        return self._height(node.left) - self._height(node.right)

    def _rotate_left(self, node: TreeNode) -> TreeNode:
        right = node.right
        node.right = right.left
        right.left = node
        self._update_height(node)
        self._update_height(right)
        return right

    def _rotate_right(self, node: TreeNode) -> TreeNode:
        left = node.left
        node.left = left.right
        left.right = node
        self._update_height(node)
        self._update_height(left)
        return left

    def _balance(self, node: TreeNode) -> TreeNode:
        self._update_height(node)
        if self._balance_factor(node) > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if self._balance_factor(node) < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def _put(self, node: Optional[TreeNode], key: Any, value: Any) -> TreeNode:
        if node is None:
            return TreeNode(key, value)
        if key < node.key:
            node.left = self._put(node.left, key, value)
        elif key > node.key:
            node.right = self._put(node.right, key, value)
        else:
            node.value = value
        return self._balance(node)

    def put(self, key: Any, value: Any) -> void:
        self.root = self._put(self.root, key, value)

    def _get(self, node: Optional[TreeNode], key: Any) -> Union[void, Any]:
        if node is None:
            return None
        if key < node.key:
            return self._get(node.left, key)
        elif key > node.key:
            return self._get(node.right, key)
        else:
            return node.value

    def get(self, key: Any) -> Union[void, Any]:
        return self._get(self.root, key)

    def _inorder(self, node: Optional[TreeNode], result: List) -> void:
        if node is not None:
            self._inorder(node.left, result)
            result.append((node.key, node.value))
            self._inorder(node.right, result)

    def items(self) -> List:
        result = []
        self._inorder(self.root, result)
        return result