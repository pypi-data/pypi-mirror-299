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
This module implements the Observer design pattern, which allows objects to be notified of changes in other objects.

Classes:
    Observer: Defines an interface for objects that should be notified of changes in a subject.
    Subject: Maintains a list of observers and notifies them of any changes.

Classes:
    Observer:
        Methods:
            update(subject: object): Updates the observer object when the subject object is updated.

    Subject:
        Methods:
            __init__(): Initializes the subject object.
            attach(observer: Observer): Attaches the observer object to the subject object.
            detach(observer: Observer): Detaches the observer object from the subject object.
            notify(): Notifies all the attached observer objects.
"""

__all__ = ['Observer', 'Subject']


class Observer(object):
    """
    Observer class that will be used to update the observer object when the subject object is updated
    """

    def update(self, subject: object):
        """
        Updates the observer object when the subject object is updated
        :param subject: subject object that is updated
        :return: None
        """
        pass


class Subject(object):
    """
    Subject class that will be used to update the observer object when the subject object is updated
    """

    def __init__(self):
        """
        Initializes the subject object
        """
        self._observers = []

    def attach(self, observer: Observer):
        """
        Attaches the observer object to the subject object
        :param observer: observer object that is attached to the subject object
        :return: None
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        """
        Detaches the observer object from the subject object
        :param observer: observer object that is detached from the subject object
        :return: None
        """
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self):
        """
        Notifies all the attached observer objects
        :return: None
        """
        for observer in self._observers:
            observer.update(self)
