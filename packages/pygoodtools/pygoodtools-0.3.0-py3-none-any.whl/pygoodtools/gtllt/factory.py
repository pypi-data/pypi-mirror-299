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
__all__ = ['CallbackFactory']

"""
Factory class to create objects.

This module provides a `CallbackFactory` class that allows for the registration
and creation of objects based on events. It maintains a registry of event names
and their corresponding callback functions.

Classes:
    CallbackFactory: A factory class to register events and create objects based on those events.

Usage Example:
    factory = CallbackFactory()
    factory.register('event_name', callback_function)
    obj = factory.create('event_name', *args, **kwargs)

CallbackFactory Methods:
    __init__(): Initializes the factory with an empty registry.
    register(event: str, callback: callable): Registers a new event with its corresponding callback function.
    create(event: str, *args, **kwargs): Creates an object based on the registered event and provided arguments.

Raises:
    ValueError: If the event is not registered in the factory.
"""
class CallbackFactory(object):
    """
    Factory class to create objects
    """

    def __init__(self):
        """
        Constructor of the class Factory
        """
        self._creators = {}

    def register(self, event: str, callback: callable):
        """
        Register a new event
        :param event: event name
        :param callback: callback function
        :return:
        """
        self._creators[event] = callback

    def create(self, event: str, *args, **kwargs):
        """
        Create an object
        :param event: event name
        :param args: arguments
        :param kwargs: keyword arguments
        :return:
        """
        if event in self._creators:
            return self._creators[event](*args, **kwargs)
        else:
            raise ValueError("Event {} not registered".format(event))
