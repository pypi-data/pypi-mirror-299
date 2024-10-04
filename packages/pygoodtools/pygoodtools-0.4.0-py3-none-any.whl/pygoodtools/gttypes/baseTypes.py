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
This module defines two classes, `Void` and `Pointer`, which serve as base types for various operations.
Classes:
    Void:
        Methods:
            __init__(*args, **kwargs):
                Initialize the Void instance.
            __getattr__(name):
            __call__(*args, **kwargs):
            _void_method(*args, **kwargs):
            __repr__():
            __str__():
            __bool__():
            __eq__(other):
            __ne__(other):
            __len__():
            __contains__(item):
            __iter__():
            __getitem__(key):
            __setitem__(key, value):
            __delitem__(key):
            __add__(other):
            __sub__(other):
            __mul__(other):
            __truediv__(other):
            __floordiv__(other):
            __mod__(other):
            __pow__(other, modulo=None):
            __and__(other):
            __or__(other):
            __xor__(other):
            __invert__():
            __lshift__(other):
            __rshift__(other):
            __lt__(other):
            __le__(other):
            __gt__(other):
            __ge__(other):
    Pointer:
        Attributes:
            obj (object): The object to which the pointer points.
        Methods:
            __getattr__(name):
            __setattr__(name, value):
            __delattr__(name):
            __call__(*args, **kwargs):
            __repr__():
            __str__():
            __bool__():
            __eq__(other):
            __ne__(other):
            __len__():
            __contains__(item):
            __iter__():
            __getitem__(key):
            __setitem__(key, value):
            __delitem__(key):
            __add__(other):
            __sub__(other):
            __mul__(other):
            __truediv__(other):
            __floordiv__(other):
            __mod__(other):
            __pow__(other, modulo=None):
            __and__(other):
            __or__(other):
            __xor__(other):
            __invert__():
            __lshift__(other):
            __rshift__(other):
            __lt__(other):
            __le__(other):
            __gt__(other):
            __ge__(other):"""
from dataclasses import dataclass
from typing import final
from abc import ABCMeta, ABC
__all__ = [
    'Void', 
    'Pointer', 
    'UInt8',
    'UInt16',
    'UInt32',
    'UInt64',
    'Int8',
    'Int16',
    'Int32',
    'Int64',
    'Char',
    'String',
    'NULL',
    'nullptr',
    'Bool',
    'Float2',
    'Float4',
    'Float8',
    'Float16',
    'Float32',
    'Float64',
    'Float128'
]

@dataclass
@final
class Void:
    """
    A class that represents a 'void' type, which essentially does nothing.
    It can be used as a placeholder or a default value where no action is required.
    """
    _instance = None
   
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Void, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, *args, **kwargs):
        pass

    def __getattr__(self, name):
        """
        Return a method that does nothing for any attribute access.
        """
        return self._void_method

    def __call__(self, *args, **kwargs):
        """
        Allow the instance to be called like a function, but do nothing.
        """
        return self

    def _void_method(self, *args, **kwargs):
        """
        A method that does nothing and returns the instance itself.
        """
        return self

    def __repr__(self):
        """
        Return a string representation of the instance.
        """
        return "<Void>"

    def __str__(self):
        """
        Return a string representation of the instance.
        """
        return "Void"

    def __bool__(self):
        """
        Always return False when evaluated in a boolean context.
        """
        return False

    def __eq__(self, other):
        """
        Check equality with another instance.
        """
        return isinstance(other, Void) or isinstance(other, NULL) or isinstance(other, nullptr)

    def __ne__(self, other):
        """
        Check inequality with another instance.
        """
        return not self.__eq__(other)

    def __len__(self):
        """
        Always return 0 for the length.
        """
        return 0

    def __contains__(self, item):
        """
        Always return False for containment checks.
        """
        return False

    def __iter__(self):
        """
        Return an empty iterator.
        """
        return iter([])

    def __getitem__(self, key):
        """
        Return the instance itself for any key access.
        """
        return self

    def __setitem__(self, key, value):
        """
        Do nothing for item assignment.
        """
        pass

    def __delitem__(self, key):
        """
        Do nothing for item deletion.
        """
        pass

    def __add__(self, other):
        """
        Return the instance itself for addition.
        """
        return self

    def __sub__(self, other):
        """
        Return the instance itself for subtraction.
        """
        return self

    def __mul__(self, other):
        """
        Return the instance itself for multiplication.
        """
        return self

    def __truediv__(self, other):
        """
        Return the instance itself for true division.
        """
        return self

    def __floordiv__(self, other):
        """
        Return the instance itself for floor division.
        """
        return self

    def __mod__(self, other):
        """
        Return the instance itself for modulo operation.
        """
        return self

    def __pow__(self, other, modulo=None):
        """
        Return the instance itself for power operation.
        """
        return self

    def __and__(self, other):
        """
        Return the instance itself for bitwise AND operation.
        """
        return self

    def __or__(self, other):
        """
        Return the instance itself for bitwise OR operation.
        """
        return self

    def __xor__(self, other):
        """
        Return the instance itself for bitwise XOR operation.
        """
        return self

    def __invert__(self):
        """
        Return the instance itself for bitwise inversion.
        """
        return self

    def __lshift__(self, other):
        """
        Return the instance itself for left shift operation.
        """
        return self

    def __rshift__(self, other):
        """
        Return the instance itself for right shift operation.
        """
        return self

    def __lt__(self, other):
        """
        Always return False for less than comparison.
        """
        return False

    def __le__(self, other):
        """
        Always return False for less than or equal comparison.
        """
        return False

    def __gt__(self, other):
        """
        Always return False for greater than comparison.
        """
        return False

    def __ge__(self, other):
        """
        Always return False for greater than or equal comparison.
        """
        return False
    

@dataclass
@final
class Pointer:
    """
    A class that represents a pointer to an object.
    It can be used to reference and manipulate the object it points to.
    """

    obj: object

    def __getattr__(self, name):
        """
        Delegate attribute access to the pointed object.
        """
        return getattr(self.ptr, name)

    def __setattr__(self, name, value):
        """
        Delegate attribute setting to the pointed object, except for 'ptr'.
        """
        if name == 'ptr':
            super().__setattr__(name, value)
        else:
            setattr(self.ptr, name, value)

    def __delattr__(self, name):
        """
        Delegate attribute deletion to the pointed object.
        """
        delattr(self.ptr, name)

    def __call__(self, *args, **kwargs):
        """
        Allow the instance to be called like a function, delegating to the pointed object.
        """
        return self.ptr(*args, **kwargs)

    def __repr__(self):
        """
        Return a string representation of the pointer.
        """
        return f"<Pointer to {repr(self.ptr)}>"

    def __str__(self):
        """
        Return a string representation of the pointed object.
        """
        return str(self.ptr)

    def __bool__(self):
        """
        Return the boolean value of the pointed object.
        """
        return bool(self.ptr)

    def __eq__(self, other):
        """
        Check equality with another pointer or object.
        """
        if isinstance(other, Pointer):
            return self.ptr == other.ptr
        return self.ptr == other

    def __ne__(self, other):
        """
        Check inequality with another pointer or object.
        """
        return not self.__eq__(other)

    def __len__(self):
        """
        Return the length of the pointed object if applicable.
        """
        return len(self.ptr)

    def __contains__(self, item):
        """
        Check if the item is in the pointed object if applicable.
        """
        return item in self.ptr

    def __iter__(self):
        """
        Return an iterator for the pointed object if applicable.
        """
        return iter(self.ptr)

    def __getitem__(self, key):
        """
        Get an item from the pointed object if applicable.
        """
        return self.ptr[key]

    def __setitem__(self, key, value):
        """
        Set an item in the pointed object if applicable.
        """
        self.ptr[key] = value

    def __delitem__(self, key):
        """
        Delete an item from the pointed object if applicable.
        """
        del self.ptr[key]

    def __add__(self, other):
        """
        Add another object to the pointed object if applicable.
        """
        return self.ptr + other

    def __sub__(self, other):
        """
        Subtract another object from the pointed object if applicable.
        """
        return self.ptr - other

    def __mul__(self, other):
        """
        Multiply the pointed object by another object if applicable.
        """
        return self.ptr * other

    def __truediv__(self, other):
        """
        Divide the pointed object by another object if applicable.
        """
        return self.ptr / other

    def __floordiv__(self, other):
        """
        Floor divide the pointed object by another object if applicable.
        """
        return self.ptr // other

    def __mod__(self, other):
        """
        Get the modulo of the pointed object by another object if applicable.
        """
        return self.ptr % other

    def __pow__(self, other, modulo=None):
        """
        Raise the pointed object to the power of another object if applicable.
        """
        return pow(self.ptr, other, modulo)

    def __and__(self, other):
        """
        Perform bitwise AND with the pointed object if applicable.
        """
        return self.ptr & other

    def __or__(self, other):
        """
        Perform bitwise OR with the pointed object if applicable.
        """
        return self.ptr | other

    def __xor__(self, other):
        """
        Perform bitwise XOR with the pointed object if applicable.
        """
        return self.ptr ^ other

    def __invert__(self):
        """
        Perform bitwise inversion on the pointed object if applicable.
        """
        return ~self.ptr

    def __lshift__(self, other):
        """
        Perform left shift on the pointed object if applicable.
        """
        return self.ptr << other

    def __rshift__(self, other):
        """
        Perform right shift on the pointed object if applicable.
        """
        return self.ptr >> other

    def __lt__(self, other):
        """
        Check if the pointed object is less than another object.
        """
        return self.ptr < other

    def __le__(self, other):
        """
        Check if the pointed object is less than or equal to another object.
        """
        return self.ptr <= other

    def __gt__(self, other):
        """
        Check if the pointed object is greater than another object.
        """
        return self.ptr > other

    def __ge__(self, other):
        """
        Check if the pointed object is greater than or equal to another object.
        """
        return self.ptr >= other
class BaseInt(ABC):
    """
    An abstract base class that represents a signed integer.
    """
    def __new__(cls, value=0, bit_size=8):
        if isinstance(value, cls):
            return value
        instance = super(BaseInt, cls).__new__(cls)
        instance._bit_size = bit_size
        instance.value = value
        return instance
    def __init__(self, value=0, bit_size=8):
        self._bit_size = bit_size
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        min_value = -(1 << (self._bit_size - 1))
        max_value = (1 << (self._bit_size - 1)) - 1
        if not (min_value <= new_value <= max_value):
            raise ValueError(f"Value must be between {min_value} and {max_value} inclusive.")
        self._value = new_value

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"

    def __str__(self):
        return str(self.value)

    def __int__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, BaseInt):
            return self.value == other.value
        return self.value == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        if isinstance(other, BaseInt):
            other = other.value
        return self.__class__((self.value + other) & ((1 << self._bit_size) - 1))

    def __sub__(self, other):
        if isinstance(other, BaseInt):
            other = other.value
        return self.__class__((self.value - other) & ((1 << self._bit_size) - 1))

    def __mul__(self, other):
        if isinstance(other, BaseInt):
            other = other.value
        return self.__class__((self.value * other) & ((1 << self._bit_size) - 1))

    def __truediv__(self, other):
        if isinstance(other, BaseInt):
            other = other.value
        if other == 0:
            raise ZeroDivisionError("division by zero")
        return self.__class__(self.value // other)

    def __floordiv__(self, other):
        return self.__truediv__(other)

    def __mod__(self, other):
        if isinstance(other, BaseInt):
            other = other.value
        return self.__class__(self.value % other)

    def __pow__(self, other, modulo=None):
        if isinstance(other, BaseInt):
            other = other.value
        return self.__class__(pow(self.value, other, modulo))

    def __and__(self, other):
        if isinstance(other, BaseInt):
            other = other.value
        return self.__class__(self.value & other)

    def __or__(self, other):
        if isinstance(other, BaseInt):
            other = other.value
        return self.__class__(self.value | other)

    def __xor__(self, other):
        if isinstance(other, BaseInt):
            other = other.value
        return self.__class__(self.value ^ other)

    def __invert__(self):
        return self.__class__(~self.value & ((1 << self._bit_size) - 1))

    def __lshift__(self, other):
        if isinstance(other, BaseInt):
            other = other.value
        return self.__class__((self.value << other) & ((1 << self._bit_size) - 1))

    def __rshift__(self, other):
        if isinstance(other, BaseInt):
            other = other.value
        return self.__class__(self.value >> other)

    def __lt__(self, other):
        if isinstance(other, BaseInt):
            other = other.value
        return self.value < other

    def __le__(self, other):
        if isinstance(other, BaseInt):
            other = other.value
        return self.value <= other

    def __gt__(self, other):
        if isinstance(other, BaseInt):
            other = other.value
        return self.value > other

    def __ge__(self, other):
        if isinstance(other, BaseInt):
            other = other.value
        return self.value >= other        
    def __int__(self):
        return self.value
    
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        original_new = cls.__new__

        def new(cls, value=0, bit_size=8):
            if isinstance(value, cls):
                return value
            return original_new(cls, value, bit_size)

        cls.__new__ = new
        
class BaseUInt(BaseInt):
    """
    An abstract base class that represents an unsigned integer.
    """

    def __init__(self, value=0, bit_size=8):
        super().__init__(value, bit_size)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        min_value = 0
        max_value = (1 << self._bit_size) - 1
        if not (min_value <= new_value <= max_value):
            raise ValueError(f"Value must be between {min_value} and {max_value} inclusive.")
        self._value = new_value
        
class UInt8(BaseUInt):
    """
    A class that represents an 8-bit unsigned integer.
    """
    def __new__(cls, value=0, bit_size=8):
        # Если значение - int, конвертируем его в UInt8, проверяя битность
        if isinstance(value, int):
            value = value & 0xFF  # Оставляем только 8 бит
        return super().__new__(cls, value, bit_size)
    
    def __init__(self, value=0):
        super().__init__(value, bit_size=8)
        
    def to_bytes(self):
        """
        Return the value as a byte.
        """
        return self.value.to_bytes(1, byteorder='big')

    @classmethod
    def from_bytes(cls, byte_data):
        """
        Create an instance from a byte.
        """
        if len(byte_data) != 1:
            raise ValueError("Byte data must be exactly 1 byte long.")
        return cls(int.from_bytes(byte_data, byteorder='big'))

    def __repr__(self):
        """
        Return a string representation of the instance.
        """
        return f"UInt8({self.value})"

    def __hash__(self):
        """
        Return the hash of the value.
        """
        return hash(self.value)
    
    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if isinstance(value, int):
            # Преобразуем целое число в объект UInt8
            value = UInt8(value)
        elif not isinstance(value, UInt8):
            raise ValueError("Assigned value must be an instance of int or UInt8.")
        # Устанавливаем значение в атрибуте `_value`
        instance.__dict__['_value'] = value
        
class UInt16(BaseUInt):
    """
    A class that represents a 16-bit unsigned integer.
    """
    def __new__(cls, value=0, bit_size=16):
        # Если значение - int, конвертируем его в UInt8, проверяя битность
        if isinstance(value, int):
            value = value & 0xFFFF  # Оставляем только 8 бит
        return super().__new__(cls, value, bit_size)
    
    def __init__(self, value=0):
        super().__init__(value, bit_size=16)
        
    def to_bytes(self):
        """
        Return the value as bytes.
        """
        return self.value.to_bytes(2, byteorder='big')

    @classmethod
    def from_bytes(cls, byte_data):
        """
        Create an instance from bytes.
        """
        if len(byte_data) != 2:
            raise ValueError("Byte data must be exactly 2 bytes long.")
        return cls(int.from_bytes(byte_data, byteorder='big'))

    def __repr__(self):
        """
        Return a string representation of the instance.
        """
        return f"UInt16({self.value})"

    def __hash__(self):
        """
        Return the hash of the value.
        """
        return hash(self.value)
    
    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if isinstance(value, int):
            # Преобразуем целое число в объект UInt8
            value = UInt8(value)
        elif not isinstance(value, UInt8):
            raise ValueError("Assigned value must be an instance of int or UInt8.")
        # Устанавливаем значение в атрибуте `_value`
        instance.__dict__['_value'] = value
        
class UInt32(BaseUInt):
    """
    A class that represents a 32-bit unsigned integer.
    """
    def __new__(cls, value=0, bit_size=16):
        # Если значение - int, конвертируем его в UInt8, проверяя битность
        if isinstance(value, int):
            value = value & 0xFFFFFFFF  # Оставляем только 8 бит
        return super().__new__(cls, value, bit_size)
    
    def __init__(self, value=0):
        super().__init__(value, bit_size=32)
        
    def to_bytes(self):
        """
        Return the value as bytes.
        """
        return self.value.to_bytes(4, byteorder='big')

    @classmethod
    def from_bytes(cls, byte_data):
        """
        Create an instance from bytes.
        """
        if len(byte_data) != 4:
            raise ValueError("Byte data must be exactly 4 bytes long.")
        return cls(int.from_bytes(byte_data, byteorder='big'))

    def __repr__(self):
        """
        Return a string representation of the instance.
        """
        return f"UInt32({self.value})"

    def __hash__(self):
        """
        Return the hash of the value.
        """
        return hash(self.value)
    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if isinstance(value, int):
            # Преобразуем целое число в объект UInt8
            value = UInt8(value)
        elif not isinstance(value, UInt8):
            raise ValueError("Assigned value must be an instance of int or UInt8.")
        # Устанавливаем значение в атрибуте `_value`
        instance.__dict__['_value'] = value
        
class UInt64(BaseUInt):
    """
    A class that represents a 64-bit unsigned integer.
    """
    def __new__(cls, value=0, bit_size=16):
        # Если значение - int, конвертируем его в UInt8, проверяя битность
        if isinstance(value, int):
            value = value & 0xFFFFFFFFFFFFFFFF  # Оставляем только 8 бит
        return super().__new__(cls, value, bit_size)
    
    def __init__(self, value=0):
        super().__init__(value, bit_size=64)
        
    def to_bytes(self):
        """
        Return the value as bytes.
        """
        return self.value.to_bytes(8, byteorder='big')

    @classmethod
    def from_bytes(cls, byte_data):
        """
        Create an instance from bytes.
        """
        if len(byte_data) != 8:
            raise ValueError("Byte data must be exactly 8 bytes long.")
        return cls(int.from_bytes(byte_data, byteorder='big'))

    def __repr__(self):
        """
        Return a string representation of the instance.
        """
        return f"UInt64({self.value})"

    def __hash__(self):
        """
        Return the hash of the value.
        """
        return hash(self.value)
    
    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if isinstance(value, int):
            # Преобразуем целое число в объект UInt8
            value = UInt8(value)
        elif not isinstance(value, UInt8):
            raise ValueError("Assigned value must be an instance of int or UInt8.")
        # Устанавливаем значение в атрибуте `_value`
        instance.__dict__['_value'] = value
        

class Int8(BaseInt):
    """
    A class that represents an 8-bit signed integer.
    """

    def __init__(self, value=0):
        super().__init__(value, bit_size=8)
        
    def to_bytes(self):
        """
        Return the value as a byte.
        """
        return self.value.to_bytes(1, byteorder='big', signed=True)

    @classmethod
    def from_bytes(cls, byte_data):
        """
        Create an instance from a byte.
        """
        if len(byte_data) != 1:
            raise ValueError("Byte data must be exactly 1 byte long.")
        return cls(int.from_bytes(byte_data, byteorder='big', signed=True))

    def __repr__(self):
        """
        Return a string representation of the instance.
        """
        return f"Int8({self.value})"

    def __hash__(self):
        """
        Return the hash of the value.
        """
        return hash(self.value)
    
    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if isinstance(value, int):
            # Преобразуем целое число в объект UInt8
            value = UInt8(value)
        elif not isinstance(value, UInt8):
            raise ValueError("Assigned value must be an instance of int or UInt8.")
        # Устанавливаем значение в атрибуте `_value`
        instance.__dict__['_value'] = value
class Int16(BaseInt):
    """
    A class that represents a 16-bit signed integer.
    """

    def __init__(self, value=0):
        super().__init__(value, bit_size=16)
        
    def to_bytes(self):
        """
        Return the value as bytes.
        """
        return self.value.to_bytes(2, byteorder='big', signed=True)

    @classmethod
    def from_bytes(cls, byte_data):
        """
        Create an instance from bytes.
        """
        if len(byte_data) != 2:
            raise ValueError("Byte data must be exactly 2 bytes long.")
        return cls(int.from_bytes(byte_data, byteorder='big', signed=True))

    def __repr__(self):
        """
        Return a string representation of the instance.
        """
        return f"Int16({self.value})"

    def __hash__(self):
        """
        Return the hash of the value.
        """
        return hash(self.value)
    
    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if isinstance(value, int):
            # Преобразуем целое число в объект UInt8
            value = UInt8(value)
        elif not isinstance(value, UInt8):
            raise ValueError("Assigned value must be an instance of int or UInt8.")
        # Устанавливаем значение в атрибуте `_value`
        instance.__dict__['_value'] = value
        
class Int32(BaseInt):
    """
    A class that represents a 32-bit signed integer.
    """

    def __init__(self, value=0):
        super().__init__(value, bit_size=32)
        
    def to_bytes(self):
        """
        Return the value as bytes.
        """
        return self.value.to_bytes(4, byteorder='big', signed=True)

    @classmethod
    def from_bytes(cls, byte_data):
        """
        Create an instance from bytes.
        """
        if len(byte_data) != 4:
            raise ValueError("Byte data must be exactly 4 bytes long.")
        return cls(int.from_bytes(byte_data, byteorder='big', signed=True))

    def __repr__(self):
        """
        Return a string representation of the instance.
        """
        return f"Int32({self.value})"

    def __hash__(self):
        """
        Return the hash of the value.
        """
        return hash(self.value)
    
    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if isinstance(value, int):
            # Преобразуем целое число в объект UInt8
            value = UInt8(value)
        elif not isinstance(value, UInt8):
            raise ValueError("Assigned value must be an instance of int or UInt8.")
        # Устанавливаем значение в атрибуте `_value`
        instance.__dict__['_value'] = value
        
class Int64(BaseInt):
    """
    A class that represents a 64-bit signed integer.
    """

    def __init__(self, value=0):
        super().__init__(value, bit_size=64)
        
    def to_bytes(self):
        """
        Return the value as bytes.
        """
        return self.value.to_bytes(8, byteorder='big', signed=True)

    @classmethod
    def from_bytes(cls, byte_data):
        """
        Create an instance from bytes.
        """
        if len(byte_data) != 8:
            raise ValueError("Byte data must be exactly 8 bytes long.")
        return cls(int.from_bytes(byte_data, byteorder='big', signed=True))

    def __repr__(self):
        """
        Return a string representation of the instance.
        """
        return f"Int64({self.value})"

    def __hash__(self):
        """
        Return the hash of the value.
        """
        return hash(self.value)
    
    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if isinstance(value, int):
            # Преобразуем целое число в объект UInt8
            value = UInt8(value)
        elif not isinstance(value, UInt8):
            raise ValueError("Assigned value must be an instance of int or UInt8.")
        # Устанавливаем значение в атрибуте `_value`
        instance.__dict__['_value'] = value   
        
class BaseChar(ABC):
    """
    An abstract base class that represents a character.
    """

    def __init__(self, value=''):
        if len(value) != 1:
            raise ValueError("Value must be a single character.")
        self.value = value

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.value}')"

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, BaseChar):
            return self.value == other.value
        return self.value == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, BaseChar):
            other = other.value
        return self.value < other

    def __le__(self, other):
        if isinstance(other, BaseChar):
            other = other.value
        return self.value <= other

    def __gt__(self, other):
        if isinstance(other, BaseChar):
            other = other.value
        return self.value > other

    def __ge__(self, other):
        if isinstance(other, BaseChar):
            other = other.value
        return self.value >= other

    def __hash__(self):
        return hash(self.value)

class Char(BaseChar):
    """
    A class that represents a character.
    """

    def __init__(self, value=''):
        super().__init__(value)

    def to_bytes(self):
        """
        Return the value as a byte.
        """
        return self.value.encode('utf-8')

    @classmethod
    def from_bytes(cls, byte_data):
        """
        Create an instance from a byte.
        """
        if len(byte_data) != 1:
            raise ValueError("Byte data must be exactly 1 byte long.")
        return cls(byte_data.decode('utf-8'))

    def __repr__(self):
        """
        Return a string representation of the instance.
        """
        return f"Char('{self.value}')"
    
class String(BaseChar, metaclass=ABCMeta):
    """
    A class that represents a string of characters.
    """

    def __init__(self, value=''):
        if not isinstance(value, str):
            raise ValueError("Value must be a string.")
        self.value = value

    def to_bytes(self):
        """
        Return the value as bytes.
        """
        return self.value.encode('utf-8')

    @classmethod
    def from_bytes(cls, byte_data):
        """
        Create an instance from bytes.
        """
        return cls(byte_data.decode('utf-8'))

    def __repr__(self):
        """
        Return a string representation of the instance.
        """
        return f"String('{self.value}')"

    def __hash__(self):
        """
        Return the hash of the value.
        """
        return hash(self.value)

    def __len__(self):
        """
        Return the length of the string.
        """
        return len(self.value)

    def __getitem__(self, key):
        """
        Get an item from the string.
        """
        return self.value[key]

    def __setitem__(self, key, value):
        """
        Set an item in the string.
        """
        if not isinstance(value, str) or len(value) != 1:
            raise ValueError("Value must be a single character.")
        self.value = self.value[:key] + value + self.value[key + 1:]

    def __delitem__(self, key):
        """
        Delete an item from the string.
        """
        self.value = self.value[:key] + self.value[key + 1:]

    def __contains__(self, item):
        """
        Check if the item is in the string.
        """
        return item in self.value

    def __iter__(self):
        """
        Return an iterator for the string.
        """
        return iter(self.value)

    def __add__(self, other):
        """
        Add another string to this string.
        """
        if not isinstance(other, str):
            raise ValueError("Can only concatenate str (not {}) to str".format(type(other).__name__))
        return String(self.value + other)

    def __mul__(self, other):
        """
        Multiply the string by an integer.
        """
        if not isinstance(other, int):
            raise ValueError("Can't multiply sequence by non-int of type '{}'".format(type(other).__name__))
        return String(self.value * other)

    def __rmul__(self, other):
        """
        Multiply the string by an integer (reversed).
        """
        return self.__mul__(other)

    def __eq__(self, other):
        """
        Check equality with another string.
        """
        if isinstance(other, String):
            return self.value == other.value
        return self.value == other

    def __ne__(self, other):
        """
        Check inequality with another string.
        """
        return not self.__eq__(other)

    def __lt__(self, other):
        """
        Check if this string is less than another string.
        """
        if isinstance(other, String):
            return self.value < other.value
        return self.value < other

    def __le__(self, other):
        """
        Check if this string is less than or equal to another string.
        """
        if isinstance(other, String):
            return self.value <= other.value
        return self.value <= other

    def __gt__(self, other):
        """
        Check if this string is greater than another string.
        """
        if isinstance(other, String):
            return self.value > other.value
        return self.value > other

    def __ge__(self, other):
        """
        Check if this string is greater than or equal to another string.
        """
        if isinstance(other, String):
            return self.value >= other.value
        return self.value >= other

class NULL:
    """
    A class that represents a NULL value.
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(NULL, cls).__new__(cls)
        return cls._instance

    def __repr__(self):
        return "NULL()"

    def __str__(self):
        return "NULL"

    def __bool__(self):
        return False

    def __eq__(self, other):
        return isinstance(other, NULL) or isinstance(other, Void) or isinstance(other, nullptr)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return False

    def __le__(self, other):
        return self.__eq__(other)

    def __gt__(self, other):
        return False

    def __ge__(self, other):
        return self.__eq__(other)

    def __hash__(self):
        return hash(None)

class nullptr:
    """
    A class that represents a nullptr value.
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(nullptr, cls).__new__(cls)
        return cls._instance

    def __repr__(self):
        return "nullptr()"

    def __str__(self):
        return "nullptr"

    def __bool__(self):
        return False

    def __eq__(self, other):
        return isinstance(other, nullptr) or isinstance(other, Void) or isinstance(other, NULL)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return False

    def __le__(self, other):
        return self.__eq__(other)

    def __gt__(self, other):
        return False

    def __ge__(self, other):
        return self.__eq__(other)

    def __hash__(self):
        return hash(None)
    
class BaseFloat(ABC):
    """
    An abstract base class that represents a floating-point number.
    """

    def __init__(self, value=0.0, bit_size=32):
        self._bit_size = bit_size
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = float(new_value)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"

    def __str__(self):
        return str(self.value)

    def __float__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, BaseFloat):
            return self.value == other.value
        return self.value == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        if isinstance(other, BaseFloat):
            other = other.value
        return self.__class__(self.value + other)

    def __sub__(self, other):
        if isinstance(other, BaseFloat):
            other = other.value
        return self.__class__(self.value - other)

    def __mul__(self, other):
        if isinstance(other, BaseFloat):
            other = other.value
        return self.__class__(self.value * other)

    def __truediv__(self, other):
        if isinstance(other, BaseFloat):
            other = other.value
        if other == 0:
            raise ZeroDivisionError("division by zero")
        return self.__class__(self.value / other)

    def __floordiv__(self, other):
        return self.__class__(self.value // other)

    def __mod__(self, other):
        if isinstance(other, BaseFloat):
            other = other.value
        return self.__class__(self.value % other)

    def __pow__(self, other, modulo=None):
        if isinstance(other, BaseFloat):
            other = other.value
        return self.__class__(pow(self.value, other, modulo))

    def __lt__(self, other):
        if isinstance(other, BaseFloat):
            other = other.value
        return self.value < other

    def __le__(self, other):
        if isinstance(other, BaseFloat):
            other = other.value
        return self.value <= other

    def __gt__(self, other):
        if isinstance(other, BaseFloat):
            other = other.value
        return self.value > other

    def __ge__(self, other):
        if isinstance(other, BaseFloat):
            other = other.value
        return self.value >= other

class Float2(BaseFloat):
    """
    A class that represents a 2-bit floating-point number.
    """

    def __init__(self, value=0.0):
        super().__init__(value, bit_size=2)

class Float4(BaseFloat):
    """
    A class that represents a 4-bit floating-point number.
    """

    def __init__(self, value=0.0):
        super().__init__(value, bit_size=4)

class Float8(BaseFloat):
    """
    A class that represents an 8-bit floating-point number.
    """

    def __init__(self, value=0.0):
        super().__init__(value, bit_size=8)

class Float16(BaseFloat):
    """
    A class that represents a 16-bit floating-point number.
    """

    def __init__(self, value=0.0):
        super().__init__(value, bit_size=16)

class Float32(BaseFloat):
    """
    A class that represents a 32-bit floating-point number.
    """

    def __init__(self, value=0.0):
        super().__init__(value, bit_size=32)

class Float64(BaseFloat):
    """
    A class that represents a 64-bit floating-point number.
    """

    def __init__(self, value=0.0):
        super().__init__(value, bit_size=64)
        

class Float128(BaseFloat):
    """
    A class that represents a 128-bit floating-point number.
    """

    def __init__(self, value=0.0):
        super().__init__(value, bit_size=128)

class Bool:
    """
    A class that represents a boolean value.
    """

    def __init__(self, value=False):
        if not isinstance(value, bool):
            raise ValueError("Value must be a boolean.")
        self.value = value

    def __repr__(self):
        return f"Bool({self.value})"

    def __str__(self):
        return str(self.value)

    def __bool__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, Bool):
            return self.value == other.value
        return self.value == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.value)

