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
    func (callable): The function to be called when the slot is triggered.
Methods:
    __init__(func):
        Initialize the Slot class with the given function.
            func (callable): The function to be called.
        Raises:
            ValueError: If func is None.
    __call__(*args, **kwargs):
        Call the slot function with the provided arguments.
            *args: Positional arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.
            The result of the function call.
"""

class Slot:
    """
    Slot class to be called when an event occurs.
    """
    def __init__(self, func):
        """
        Initialize the slot class.
        Args:
            func: the function to be called
        Return: 
            None
        """
        if not func:
            raise ValueError('func must not be None')
        
        self.func = func

    def __call__(self, *args, **kwargs):
        """
        Call the slot function when called
        Args:
            *args: positional arguments
            **kwargs: keyword arguments
        Returns:
            None
        """
        return self.func(*args, **kwargs)


