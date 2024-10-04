import threading
import time
from typing import Callable, List, Optional, final

@final
class ArmTimer:
    def __init__(self, 
                 interval: float, 
                 callback: Callable, 
                 single_shot: bool = False,
                 argv: Optional[List] = None,
                 *args,
                 **kwargs):
        """
        Initialize the timer.
        
        :param interval: Time interval in seconds.
        :param callback: Function to be called when the timer expires.
        :param single_shot: If True, the timer will run only once. If False, it will repeat.
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
            # Add more keyword arguments if needed

    def _run(self):
        """
        Run the timer and execute the callback function.
        """
        print('Timer is running...')
        next_call = time.perf_counter()  # More precise timer
        while not self._stop_event.is_set():
            next_call += self.interval
            time_to_sleep = next_call - time.perf_counter()
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)
            
            if self._stop_event.is_set():
                break
            
            result = self.callback(*self.argv) if self.argv else self.callback()

            if result is None:
                continue
            
            if hasattr(self, '_ext'):
                self._ext.emit(result)
            else:
                print(f"WARNING! Function {self.callback.__name__} returned a raw result, to process the result, add signal=\n")

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