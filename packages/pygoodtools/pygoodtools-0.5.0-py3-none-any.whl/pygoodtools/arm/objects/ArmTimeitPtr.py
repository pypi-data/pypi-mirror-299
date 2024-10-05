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
import functools
import time

class ArmTimeitPtr(ctypes.Structure):
    """
    A context manager and decorator for measuring the execution time of code blocks and functions.
    """
    _fields_ = [("t", ctypes.c_double), ("time_func", ctypes.CFUNCTYPE(ctypes.c_double))]

    def __init__(self, t=0.0, time_func=None):
        self.t = t
        self.time_func = time_func or time.time

    def __enter__(self):
        self.start = self.time_func()
        return self

    def __exit__(self, type, value, traceback):
        self.dt = self.time_func() - self.start
        self.t += self.dt

    def __str__(self):
        return f"Elapsed time is {self.t} s"

    @staticmethod
    def timeit(func):
        @functools.wraps(func)
        def wrapper_timeit(*args, **kwargs):
            start_time = time.time()  # Record the start time
            result = func(*args, **kwargs)  # Call the function
            end_time = time.time()  # Record the end time
            elapsed_time = end_time - start_time  # Calculate the elapsed time
            print(f"Function {func.__name__!r} with arguments {args!r} and keywords arguments {kwargs!r} executed in {elapsed_time:.4f} seconds")
            return result  # Return the result of the function

        return wrapper_timeit