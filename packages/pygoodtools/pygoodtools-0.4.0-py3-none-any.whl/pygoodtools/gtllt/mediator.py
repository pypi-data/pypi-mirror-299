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
This module defines the Mediator and BaseComponent classes.

Classes:
    Mediator: Acts as the mediator between clients and the server.
    BaseComponent: Serves as the base class for all components, utilizing a mediator for event notifications.

Mediator:
    Methods:
        notify(sender, event): Notifies the clients about the event.

BaseComponent:
    Methods:
        __init__(__mediator=None): Initializes the component with an optional mediator.
        mediator: Property to get or set the mediator.
"""
__all__ = ['Mediator']


class Mediator:
    """
    This class is the mediator between the clients and the server.
    """

    def notify(self, sender, event):
        """
        Notify the clients about the event.
        """

        pass


class BaseComponent:
    """
    This class is the base class for all components.
    """

    def __init__(self, __mediator=None):
        """
        Constructor.
        :param __mediator: The mediator. It is used to notify the clients about the event.
        """
        self._mediator = __mediator

    @property
    def mediator(self):
        """
        Get the mediator.
        """
        return self._mediator

    @mediator.setter
    def mediator(self, __mediator):
        """
        Set the mediator.
        """

        self._mediator = __mediator
