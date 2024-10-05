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
This module defines metaclasses `ConstMeta` and `MapMeta`.
Once an attribute is set, it cannot be modified or deleted.

Classes:
    ConstMeta: A metaclass that prevents rebinding and unbinding of class attributes.
    MapMeta: A metaclass that allows custom logic to be applied when creating a class.
    HashMapMeta: A metaclass that allows custom logic to be applied when creating a class.
ConstMeta:
    Methods:
        __setattr__(cls, name, value):
            Prevents rebinding of class attributes. 
            Raises a TypeError if an attempt is made to rebind an existing attribute.
        
        __delattr__(cls, name):
            Prevents unbinding of class attributes. 
            Raises a TypeError if an attempt is made to delete an existing attribute.
            
MapMeta:
    Methods:
        __new__(mcs, name, bases, dct):
            Allows custom logic to be applied when creating a class. 
            Prints a message indicating the creation of a class with the metaclass.

HashMapMeta:
    Methods: 
        __new__(mcs, name, bases, dct):
            Allows custom logic to be applied when creating a class. 
            Prints a message indicating the creation of a class with the metaclass.
"""

class ConstMeta(type):
    def __setattr__(cls, name, value):
        if name in cls.__dict__:
            raise TypeError(f"Can't rebind const({name})")
        super().__setattr__(name, value)

    def __delattr__(cls, name):
        if name in cls.__dict__:
            raise TypeError(f"Can't unbind const({name})")
        raise NameError(name)

class MapMeta(type):
    """A metaclass that allows custom logic to be applied when creating a class."""
    def __new__(mcs, name, bases, dct):
        return super().__new__(mcs, name, bases, dct)

class HashMapMeta(type):
    """A metaclass that allows custom logic to be applied when creating a class."""
    def __new__(mcs, name, bases, dct):
        dct['is_empty'] = lambda self: self.size == 0
        return super().__new__(mcs, name, bases, dct)