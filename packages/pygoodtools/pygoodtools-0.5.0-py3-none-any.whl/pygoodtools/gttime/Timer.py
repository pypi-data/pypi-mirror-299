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
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTOR
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# COPYRIGHT (c) 2024 Massonskyi

"""
Timer class to execute a callback function at specified intervals.
Attributes:
    interval (float): Time interval in seconds.
    callback (Callable): Function to be called when the timer expires.
    single_shot (bool): If True, the timer will run only once. If False, it will repeat.
    argv (Optional[List]): List of arguments to pass to the callback function.
    args (tuple): Additional positional arguments.
    kwargs (dict): Additional keyword arguments.
    _timer_thread (Optional[threading.Thread]): Thread running the timer.
    _stop_event (threading.Event): Event to stop the timer.
Methods:
    __init__(interval: float, callback: Callable, single_shot: bool = False, argv: Optional[List] = None, *args, **kwargs):
    setInterval(interval: float) -> None:
    _parse_kwargs(**kwargs):
        Parse additional keyword arguments.
    _run():
    start():
        Start the timer.
    stop():
        Stop the timer.
"""
import threading
import time
from typing import Callable, List, Optional, final

@final
class Timer:    
    def __init__(self, 
                 interval: float, 
                 callback: Callable, 
                 single_shot: bool = False,
                 argv: Optional[List] = None,
                 *args,
                 **kwargs
        ):
        """
        Initialize the timer.
        
        :param interval: Time interval in seconds.
        :param callback: Function to be called when the timer expires.
        :param single_shot: If True, the timer will run only once. If False, it will repeat.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """
        self.interval = interval
        self.callback = callback
        self.single_shot = single_shot
        self._timer_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        # Parse additional positional arguments
        self.argv = argv if argv is not None else []
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        
        self._parse_kwargs(**kwargs)
        
    def setInterval(self, interval: float) -> None:
        """
        Set the timer interval.

        :param interval: Time interval in seconds.
        """
        self.interval = interval
                
    def _parse_kwargs(self, **kwargs):
        for key, value in kwargs.items():
            if key == '_ext':
                setattr(self, key, value)
            # to add more keyword arguments here if need...

    def _run(self):
        """
        Run the timer and execute the callback function.
        """
        while not self._stop_event.is_set():
            time.sleep(self.interval)
            
            if self._stop_event.is_set():
                break
            result = self.callback(*self.argv) if self.argv else self.callback() 
                        
            if result is None:
                continue
            
            if not hasattr(self, '_ext'):
                print(f"WARNING! Function {self.callback.__name__} returned a raw result, to process the result, add signal=\n")
                continue

            self._ext.emit(result)

            if self.single_shot:
                break
    
    def start(self):
        """
        Start the timer
        """
        if self._timer_thread is None or not self._timer_thread.is_alive():
            self._stop_event.clear()
            self._timer_thread = threading.Thread(target=self._run)
            self._timer_thread.start()
        
    def stop(self):
        """
        Stop the timer
        """
        self._stop_event.set()
        if self._timer_thread is not None:
            self._timer_thread.join()