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
import functools

__all__ = ['arm_is_type', 'ArmTypeCheckParams']
__version__ = '0.1.0'
__description__ = 'Проверяет типы аргументов функции.'

class ArmTypeCheckParams(ctypes.Structure):
    _fields_ = [("types", ctypes.py_object)]

def arm_is_type(*types):
    """
    A decorator to enforce type checking on function arguments.
    Parameters:
        *types: Variable length argument list of types to check against the function arguments.
    Returns:
        decorator_type_check (function): A decorator function that wraps the original function with type checking.
    Raises:
        ValueError: If the number of arguments passed to the function does not match the number of types specified.
        TypeError: If any argument does not match the expected type.
    Example:
        @is_type(int, str)
        def example_function(a, b):
            return f"{a} is an integer and {b} is a string"
        example_function(1, "hello")  # This will work
        example_function(1, 2)        # This will raise TypeError
    """
    params = ArmTypeCheckParams(types)

    def decorator_type_check(func):
        @functools.wraps(func)
        def wrapper_type_check(*args, **kwargs):
            if len(args) != len(params.types):
                raise ValueError("Argument count does not match")
            for a, t in zip(args, params.types):
                if not isinstance(a, t):
                    raise TypeError(f"Expected {t}, got {type(a)}")
            return func(*args, **kwargs)

        return wrapper_type_check

    return decorator_type_check