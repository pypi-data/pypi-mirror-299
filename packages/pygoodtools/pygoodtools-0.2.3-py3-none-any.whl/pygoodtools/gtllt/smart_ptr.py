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
Attributes:
    obj (object): The object to be managed.

Methods:
    __init__(obj: object):
        Args:
            obj (object): The object to be managed.
    
    __enter__():
        Returns:
            object: The managed object.
    
    __exit__(exc_type, exc_val, exc_tb):
        Args:
            exc_type (type): The exception type.
            exc_val (Exception): The exception value.
            exc_tb (traceback): The exception traceback.
        Returns:
            None
"""

__all__ = ['SmartPointer']


class SmartPointer(object):
    """
    A smart pointer class.
    """
    def __init__(self, obj: object):
        """
        Initialize the smart pointer.
        :param obj: The object to be managed.
        """
        self.obj = obj

    def __enter__(self):
        """
        Enter the context.
        :return: The object.
        """
        return self.obj

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context.
        :param exc_type: The exception type.
        :param exc_val: The exception value.
        :param exc_tb: The exception traceback.
        :return: None.
        """
        del self.obj
