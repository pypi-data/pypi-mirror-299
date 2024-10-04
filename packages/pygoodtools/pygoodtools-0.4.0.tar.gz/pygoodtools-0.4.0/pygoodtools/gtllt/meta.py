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
This module defines a metaclass `Meta` and a base class `Base` that utilizes the metaclass.

Classes:
    Meta: A metaclass that adds a `registry` attribute to the class.
    Base: A base class that registers its subclasses in the `registry` attribute.

Metaclass `Meta`:
    Methods:
        __new__(cls, name, bases, attrs):
            Creates a new class and adds a `registry` attribute to it.

Base class `Base`:
    Methods:
        __init_subclass__(cls, **kwargs):
            Initializes the subclass and registers it in the `registry` attribute.
"""


class Meta(type):
    """
    Metaclass for the class.
    """

    def __new__(cls, name, bases, attrs):
        """
        Create a new class.
        """
        # Get the base class.
        cls = super().__new__(cls, name, bases, attrs)
        # Добавляем новый атрибут
        cls.registry = {}
        return cls


class Base(metaclass=Meta):
    """
    Base class for the class.
    """

    def __init_subclass__(cls, **kwargs):
        """
        Initialize the subclass.
        """
        # Добавляем новый атрибут
        super().__init_subclass__(**kwargs)
        # Регистрируем подклассы
        cls.registry[cls.__name__] = cls
