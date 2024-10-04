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
import time
import functools

__all__ = ['timeit']
__version__ = '0.1.0'
__description__ = 'Измеряет время выполнения функции.'


def timeit(func):
    """
    A decorator that measures the execution time of a function.
    This decorator wraps a function and prints the time it took to execute the function.
    It also prints the function's name, its positional arguments, and its keyword arguments.
    Args:
        func (callable): The function to be wrapped by the decorator.
    Returns:
        callable: The wrapped function that includes execution time measurement.
    Example:
        @timeit
        def example_function(param1, param2):
            # Function implementation
            pass
        example_function(1, 2)
        # Output: Function 'example_function' with arguments (1, 2) and keywords arguments {} executed in X.XXXX seconds
    """
    
    @functools.wraps(func)
    def wrapper_timeit(*args, **kwargs):
        start_time = time.time()  # Record the start time
        result = func(*args, **kwargs)  # Call the function
        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time  # Calculate the elapsed time
        print(f"Function {func.__name__!r} with arguments {args!r} and keywords arguments {kwargs!r} executed in {elapsed_time:.4f} seconds")
        return result  # Return the result of the function

    return wrapper_timeit