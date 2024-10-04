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
This module defines the Command design pattern with classes for commands and an invoker.

Classes:
    Command: Base class for all commands.
    SimpleCommand: A simple command with a name and description.
    Invoker: Executes commands before and after performing an important task.

Classes and Methods:
    Command:
        - execute: Method to be called when the command is executed.

    SimpleCommand(Command):
        - __init__: Constructor for SimpleCommand.
            Parameters:
                - name (str): The name of the command.
                - description (str): The description of the command.
        - execute: Method to be called when the command is executed.

    Invoker:
        - __init__: Constructor for Invoker.
        - set_on_start: Sets the command to be executed when the invoker starts.
            Parameters:
                - command (Command): The command to execute.
        - set_on_finish: Sets the command to be executed when the invoker finishes.
            Parameters:
                - command (Command): The command to execute.
        - do_something_important: Performs an important task, executing start and finish commands if set.
"""

__all__ = ['Command']

class Command(object):
    """
    This is the base class for all commands
    """

    def execute(self):
        """
        This is the method that will be called when the command is executed
        :return: None
        """
        pass


class SimpleCommand(Command):
    """
    This is the base class for all simple commands
    """

    def __init__(self, name, description):
        """
        This is the constructor for the SimpleCommand class
        :param name: the name of the command
        :param description: the description of the command
        """
        self.name = name
        self.description = description

    def execute(self):
        """
        This is the method that will be called when the command is executed
        :return: None
        """
        print(f"Executing command: {self.name} - {self.description}")


class Invoker(object):
    """
    This is the base class for all commands that can be executed by a user or a bot user
    """

    def __init__(self):
        """
        This is the constructor for the Invoker class
        """
        self._on_start = None
        self._on_finish = None

    def set_on_start(self, command):
        """
        This method sets the command that will be executed when the invoker starts
        :param command: the command to execute
        :return: None
        """
        self._on_start = command

    def set_on_finish(self, command):
        """
        This method sets the command that will be executed when the invoker finishes
        :param command: the command to execute
        :return: None
        """

        self._on_finish = command

    def do_something_important(self):
        """
        This method does something important
        :return: None
        """
        print('Invoker: Does anybody want something done before I begin?')
        if self._on_start:
            self._on_start.execute()

        print('Invoker: ...doing something really important...')

        print('Invoker: Does anybody want something done after I finish?')
        if self._on_finish:
            self._on_finish.execute()
