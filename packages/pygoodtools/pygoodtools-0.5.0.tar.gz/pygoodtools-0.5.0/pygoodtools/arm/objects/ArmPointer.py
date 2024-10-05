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
from typing import Any, final

class ArmPointer(ctypes.Structure):
    """
    A class that represents a pointer to an object using ctypes.
    It can be used to reference and manipulate the object it points to.
    """
    _fields_ = [("obj", ctypes.py_object)]

    def __init__(self, obj: Any) -> None:
        """
        Initialize the pointer to point to an object.
        """
        super().__init__()
        self.obj = obj

    @property
    def ptr(self) -> Any:
        """
        Return the underlying object.
        """
        return self.obj

    def __getattr__(self, name: str) -> Any:
        """
        Delegate attribute access to the pointed object.
        """
        return getattr(self.ptr, name)

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Delegate attribute setting to the pointed object.
        """
        if name == 'obj':
            super().__setattr__(name, value)
        else:
            setattr(self.ptr, name, value)

    def __delattr__(self, name: str) -> None:
        """
        Delegate attribute deletion to the pointed object.
        """
        delattr(self.ptr, name)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Allow the instance to be called like a function, delegating to the pointed object.
        """
        return self.ptr(*args, **kwargs)

    def __repr__(self) -> str:
        """
        Return a string representation of the pointer.
        """
        return f"<Pointer to {repr(self.ptr)}>"

    def __str__(self) -> str:
        """
        Return a string representation of the pointed object.
        """
        return str(self.ptr)

    def __bool__(self) -> bool:
        """
        Return the boolean value of the pointed object.
        """
        return bool(self.ptr)

    def __eq__(self, other: Any) -> bool:
        """
        Check equality with another pointer or object.
        """
        if isinstance(other, ArmPointer):
            return self.ptr == other.ptr
        return self.ptr == other

    def __ne__(self, other: Any) -> bool:
        """
        Check inequality with another pointer or object.
        """
        return not self.__eq__(other)

    def __len__(self) -> int:
        """
        Return the length of the pointed object if applicable.
        """
        return len(self.ptr)

    def __contains__(self, item: Any) -> bool:
        """
        Check if the item is in the pointed object if applicable.
        """
        return item in self.ptr

    def __iter__(self):
        """
        Return an iterator for the pointed object if applicable.
        """
        return iter(self.ptr)

    def __getitem__(self, key: Any) -> Any:
        """
        Get an item from the pointed object if applicable.
        """
        return self.ptr[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set an item in the pointed object if applicable.
        """
        self.ptr[key] = value

    def __delitem__(self, key: Any) -> None:
        """
        Delete an item from the pointed object if applicable.
        """
        del self.ptr[key]

    def __add__(self, other: Any) -> Any:
        """
        Add another object to the pointed object if applicable.
        """
        return self.ptr + other

    def __sub__(self, other: Any) -> Any:
        """
        Subtract another object from the pointed object if applicable.
        """
        return self.ptr - other

    def __mul__(self, other: Any) -> Any:
        """
        Multiply the pointed object by another object if applicable.
        """
        return self.ptr * other

    def __truediv__(self, other: Any) -> Any:
        """
        Divide the pointed object by another object if applicable.
        """
        return self.ptr / other

    def __floordiv__(self, other: Any) -> Any:
        """
        Floor divide the pointed object by another object if applicable.
        """
        return self.ptr // other

    def __mod__(self, other: Any) -> Any:
        """
        Get the modulo of the pointed object by another object if applicable.
        """
        return self.ptr % other

    def __pow__(self, other: Any, modulo: Any = None) -> Any:
        """
        Raise the pointed object to the power of another object if applicable.
        """
        return pow(self.ptr, other, modulo)

    def __and__(self, other: Any) -> Any:
        """
        Perform bitwise AND with the pointed object if applicable.
        """
        return self.ptr & other

    def __or__(self, other: Any) -> Any:
        """
        Perform bitwise OR with the pointed object if applicable.
        """
        return self.ptr | other

    def __xor__(self, other: Any) -> Any:
        """
        Perform bitwise XOR with the pointed object if applicable.
        """
        return self.ptr ^ other

    def __invert__(self) -> Any:
        """
        Perform bitwise inversion on the pointed object if applicable.
        """
        return ~self.ptr

    def __lshift__(self, other: Any) -> Any:
        """
        Perform left shift on the pointed object if applicable.
        """
        return self.ptr << other

    def __rshift__(self, other: Any) -> Any:
        """
        Perform right shift on the pointed object if applicable.
        """
        return self.ptr >> other

    def __lt__(self, other: Any) -> bool:
        """
        Check if the pointed object is less than another object.
        """
        return self.ptr < other

    def __le__(self, other: Any) -> bool:
        """
        Check if the pointed object is less than or equal to another object.
        """
        return self.ptr <= other

    def __gt__(self, other: Any) -> bool:
        """
        Check if the pointed object is greater than another object.
        """
        return self.ptr > other

    def __ge__(self, other: Any) -> bool:
        """
        Check if the pointed object is greater than or equal to another object.
        """
        return self.ptr >= other
