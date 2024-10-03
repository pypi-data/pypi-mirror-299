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
GTObject is an abstract base class that provides a framework for objects with named signals.

Attributes:
    name (str): The name of the GTObject instance.
    signals (dict): A dictionary mapping signal names to Signal objects.

Methods:
    __init__(name):
        Initializes a GTObject instance with a given name.
    
    display_info():
        Abstract method that must be implemented by subclasses to display information about the object.
    
    __str__():
        Returns a string representation of the GTObject instance.
    
    connect(signal_name, callback):
        Connects a callback function to a named signal. If the signal does not exist, it is created.
    
    disconnect(signal_name, callback):
        Disconnects a callback function from a named signal.
    
    emit(signal_name, *args, **kwargs):
        Emits a named signal, invoking all connected callback functions with the provided arguments.
"""

from abc import ABC, abstractmethod
from typing import Any

from . import Signal

class GTObject(ABC):
    """
    GTObject is an abstract base class that provides a framework for objects
    with named signals and callback connections.
    Attributes:
        name (str): The name of the GTObject instance.
        signals (dict): A dictionary mapping signal names to Signal objects.
    Methods:
        display_info():
            Abstract method that must be implemented by subclasses to display
            information about the object.
        __str__():
            Returns a string representation of the GTObject instance.
        connect(signal_name, callback):
            Connects a callback function to a named signal. If the signal does
            not exist, it is created.
        disconnect(signal_name, callback):
            Disconnects a callback function from a named signal.
        emit(signal_name, *args, **kwargs):
            Emits a named signal, invoking all connected callback functions
            with the provided arguments.
    """
    def __init__(self, name):
        self.name = name
        self.signals = {}

    @abstractmethod
    def display_info(self):
        pass

    def __str__(self):
        return f"GTObject: {self.name}"

    def connect(self, signal_name, callback):
        if signal_name not in self.signals:
            self.signals[signal_name] = Signal()
        self.signals[signal_name].connect(callback)

    def disconnect(self, signal_name, callback):
        if signal_name in self.signals:
            self.signals[signal_name].disconnect(callback)

    def emit(self, signal_name, *args, **kwargs):
        if signal_name in self.signals:
            self.signals[signal_name].emit(*args, **kwargs)