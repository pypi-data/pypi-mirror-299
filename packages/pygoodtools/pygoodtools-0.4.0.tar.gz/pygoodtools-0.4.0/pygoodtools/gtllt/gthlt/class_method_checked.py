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
__all__ = ['ensure_method_exists']
__version__ = '0.1.0'
__description__ = 'Декоратор для методов класса, позволяющий обойти отсутствие метода в родительском классе.'


def ensure_method_exists(method_name):
    """
    A decorator to ensure that a class implements a specific method.
    This decorator checks if the given method name exists in the class. If the method
    does not exist, it raises a TypeError.
    Args:
        method_name (str): The name of the method that must be implemented by the class.
    Returns:
        function: A decorator function that checks for the existence of the specified method.
    Raises:
        TypeError: If the class does not implement the specified method.
    Example:
        @ensure_method_exists('my_method')
        class MyClass:
            def my_method(self):
                pass
    """
    
    def decorator_ensure_method_exists(cls):
        if not hasattr(cls, method_name):
            raise TypeError(f"Class {cls.__name__} must implement method {method_name}")
        return cls

    return decorator_ensure_method_exists

