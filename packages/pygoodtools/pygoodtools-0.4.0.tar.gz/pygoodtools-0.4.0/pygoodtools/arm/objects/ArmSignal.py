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
from typing import Callable, final

@final
class ArmSignal:
    """
    Callback class to be called when an event occurs.
    Optimized for ARM architecture with low-level improvements.
    """

    def __init__(self) -> None:
        """
        Initialize the callback class.
        """
        # Используем ctypes для эффективного управления памятью
        # Определяем массив под указатели на функции с предварительным выделением памяти на 16 слотов
        self._slots = (ctypes.py_object * 16)()  # Массив указателей на объекты Python
        self._slot_count = ctypes.c_int(0)  # Счетчик подключенных слотов
    
    def connect(self, func: Callable) -> None:
        """
        Connect a callback to the event signals.
        """
        if not callable(func):
            raise ValueError('callback must be callable')
        
        # Добавляем функцию в свободный слот, если есть место
        if self._slot_count.value < len(self._slots):
            self._slots[self._slot_count.value] = ctypes.py_object(func)
            self._slot_count.value += 1
        else:
            raise OverflowError('Maximum number of callbacks reached')
    
    def disconnect(self, func: Callable) -> None:
        """
        Disconnect a callback from the event signals.
        """
        if not callable(func):
            raise ValueError('callback must be callable')

        # Удаление функции, минимизируя операции с памятью
        for i in range(self._slot_count.value):
            if self._slots[i] == ctypes.py_object(func):
                # Смещаем функции на одно место назад
                for j in range(i, self._slot_count.value - 1):
                    self._slots[j] = self._slots[j + 1]
                self._slots[self._slot_count.value - 1] = None  # Очищаем последний слот
                self._slot_count.value -= 1
                return
        raise ValueError('callback not connected')
        
    def emit(self, *args, **kwargs) -> None:
        """
        Emit an event.
        Args:
            *args: positional arguments
            **kwargs: keyword arguments
        """
        # Прямой вызов функций с передачей аргументов
        for i in range(self._slot_count.value):
            callback = self._slots[i]
            if callback:
                callback(*args, **kwargs)
