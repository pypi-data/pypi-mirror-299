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
from typing import Callable, Any, final

@final
class ArmCallback(ctypes.Structure):
    """
    Factory class to create objects
    """
    _fields_ = [("_creators", ctypes.py_object)]

    def __init__(self):
        """
        Constructor of the class Factory
        """
        self._creators = {}

    def register(self, event: str, callback: Callable[..., Any]) -> None:
        """
        Register a new event
        :param event: event name
        :param callback: callback function
        :return: None
        """
        if event not in self._creators:
            self._creators[event] = []
        self._creators[event].append(callback)

    def unregister(self, event: str, callback: Callable[..., Any]) -> None:
        """
        Unregister an event
        :param event: event name
        :param callback: callback function
        :return: None
        """
        if event in self._creators and callback in self._creators[event]:
            self._creators[event].remove(callback)
            if not self._creators[event]:
                del self._creators[event]

    def is_registered(self, event: str) -> bool:
        """
        Check if an event is registered
        :param event: event name
        :return: bool
        """
        return event in self._creators

    def create(self, event: str, *args, **kwargs) -> Any:
        """
        Create an object
        :param event: event name
        :param args: arguments
        :param kwargs: keyword arguments
        :return: Any
        """
        if event in self._creators:
            results = []
            for callback in self._creators[event]:
                results.append(callback(*args, **kwargs))
            return results
        else:
            raise ValueError(f"Event {event} not registered")