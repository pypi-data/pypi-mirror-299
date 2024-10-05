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
Methods:
    __init__() -> Optional[None]:
        Initialize the callback class.
    connect(func: Optional[callable] = None) -> Optional[None]:
        Connect a callback to the event signals.
            func: The callback function to connect.
        Raises:
            ValueError: If the callback is None or already connected.
    disconnect(func: Optional[callable] = None) -> Optional[None]:
        Disconnect a callback from the event signals.
            func: The callback function to disconnect.
        Raises:
            ValueError: If the callback is None or not connected.
    emit(*args: Optional[Any], **kwargs: Optional[Any]) -> Optional[None]:
        Emit an event.
            *args: Positional arguments.
            **kwargs: Keyword arguments.
    get() -> Optional[Any]:
        Get the result of the slot function when called.
            Any result or None if no result is available.
        Raises:
            ValueError: If the result is empty.
"""
from typing import Any, List, Optional, final


@final
class Signal:
    """
    Callback class to be called when an event occurs
    """
    
    def __init__(
        self
    ) -> Optional[None]:
        """
        Initialize the callback class
        """
        self._slots:        Optional[List[callable]]    =   []
        self.__result:      Optional[Any]               =   {}
        
    def connect(
        self,
        func: Optional[callable] = None
    ) -> Optional[None]:
        """
        Connect a callback to the event signals
        """
        if not func:
            raise ValueError('callback must not be None')
        
        if func in self._slots:
            raise ValueError('callback already connected')
        
        self._slots.append(func)

    def disconnect(
        self,
        func: Optional[callable] = None
    ) -> Optional[None]:
        """
        Disconnect a callback from the event signals
        """
        if not func:
            raise ValueError('callback must not be None')
        
        if func not in self._slots:
            raise ValueError('callback not connected')
        
        # self.__result.pop(self._slots.__class__.__name__)
        self._slots.remove(func)

        
    def emit(
        self,
        *args: Optional[Any],
        **kwargs: Optional[Any]
    ) -> Optional[None]:
        """
        Emit an event
        Args:
            *args: positional arguments
            **kwargs: keyword arguments
        Returns:
            None
        """
        for func in self._slots:
            res = func(*args, **kwargs)
            
            if res: 
                self.__result[func.__class__.__name__] = res

    def get(
        self,
    ) -> Optional[Any]:
        """
        Get the result of the slot function when called
        Returns:
            Any result or None if no result is available
        """
        for func in self._slots:
            if self.__result[func.__class__.__name__]:
                yield self.__result[func.__class__.__name__]
            else:
                raise ValueError(f'result {func.__class__.__name__} empty')