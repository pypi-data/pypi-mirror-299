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
A module that provides a functor class `F` for functional programming.

Classes:
    F: A class that represents a functor, allowing function chaining, mapping, filtering, currying, argument transformation, and reduction.

Example usage:



    >>> f.map(lambda x: x * 2)(2)

    >>> f.filter(lambda x: x > 2)(3)
    4

    >>> f.curry(2)(3)

    >>> f.transform_args(lambda x: (x + 1,))(2)
    4

    >>> f.reduce(lambda x, y: x + y, 0)([1, 2, 3])
    9
"""


import functools
from typing import Callable, Any, Optional

__all__ = ['F']


class F(object):
    """
    A class that represents a functor.

    >>> f = F(lambda x: x + 1)
    >>> f(1)
    2

    >>> g = F(lambda x, y: x * y, 2)
    >>> g(3)
    6

    >>> h = f.chain(g)
    >>> h(3)
    7  # f(3) + g(3)
    """

    def __init__(self, func: Callable, *args, **kwargs):
        """
        Initialize the functor.
        :param func: callable function that takes a single argument and returns a value.
        :param args: arguments to be passed to func.
        :param kwargs: keyword arguments to be passed to func.
        """
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self._cache = {}

    def __call__(self, *args, **kwargs) -> Any:
        """
        Call the functor.
        :param args: arguments to be passed to func.
        :param kwargs: keyword arguments to be passed to func.
        :return: the result of calling func with the given arguments.
        """
        combined_args = self.args + args
        combined_kwargs = {**self.kwargs, **kwargs}
        cache_key = (combined_args, frozenset(combined_kwargs.items()))

        if cache_key in self._cache:
            result = self._cache[cache_key]
        else:
            result = self.func(*combined_args, **combined_kwargs)
            self._cache[cache_key] = result

        self.log_call(combined_args, combined_kwargs, result)
        return result

    def chain(self, other_func: Callable) -> 'F':
        """
        Chain another function to the functor, applying the other function to the result.
        :param other_func: callable function to be applied to the result of the current functor.
        :return: a new functor that chains the given function to the current functor.
        """
        return F(lambda *args, **kwargs: other_func(self(*args, **kwargs)))

    def map(self, transform_func: Callable) -> 'F':
        """
        Apply a transformation function to the result of the functor.
        :param transform_func: callable function to transform the result of the functor.
        :return: a new functor with the transformation applied.
        """
        return F(lambda *args, **kwargs: transform_func(self(*args, **kwargs)))

    def filter(self, filter_func: Callable) -> 'F':
        """
        Filter the result of the functor.
        :param filter_func: callable function to filter the result of the functor.
        :return: a new functor that filters the result of the current functor.
        """
        return F(lambda *args, **kwargs: self(*args, **kwargs) if filter_func(self(*args, **kwargs)) else None)

    def curry(self, *curry_args, **curry_kwargs) -> 'F':
        """
        Partially apply arguments to the functor.
        :param curry_args: arguments to be partially applied.
        :param curry_kwargs: keyword arguments to be partially applied.
        :return: a new functor with the partially applied arguments.
        """
        return F(self.func, *(self.args + curry_args), **{**self.kwargs, **curry_kwargs})

    def transform_args(self, transform_func: Callable) -> 'F':
        """
        Transform the arguments before passing them to the functor.
        :param transform_func: callable function to transform the arguments.
        :return: a new functor with the transformed arguments.
        """
        return F(lambda *args, **kwargs: self(*transform_func(*args, **kwargs)))

    def reduce(self, reducer_func: Callable, initial: Optional[Any] = None) -> 'F':
        """
        Apply an accumulator function to the result of the functor.
        :param reducer_func: callable accumulator function.
        :param initial: initial value for the accumulator.
        :return: a new functor with the reduction applied.
        """
        if initial is None:
            return F(lambda *args, **kwargs: functools.reduce(reducer_func, self(*args, **kwargs)))
        else:
            return F(lambda *args, **kwargs: functools.reduce(reducer_func, self(*args, **kwargs), initial))

    def log_call(self, args, kwargs, result) -> None:
        """
        Log the call of the functor for debugging purposes.
        :param args: arguments passed to the functor.
        :param kwargs: keyword arguments passed to the functor.
        :param result: result of the functor call.
        """
        print(f"Calling {self.func.__name__} with args {args} and kwargs {kwargs} resulted in {result}")

    def clear_cache(self) -> None:
        """
        Clear the cache of the functor.
        """
        self._cache.clear()
