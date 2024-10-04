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
This module provides a collection of utility decorators and functions for various purposes such as caching, 
method existence checking, context management, logging, memoization, timing, singleton pattern, type checking, 
and retry mechanisms.

Available Decorators and Functions:
- pyGTCache: LRU (Least Recently Used) cache decorator.
- pyGTEnsureMethodExists: Decorator to ensure a method exists in a class.
- pyGTContextManager: Context manager decorator.
- pyGTLogCalls: Decorator to log function calls.
- pyGTMemoize: Memoization decorator to cache function results.
- pyGTTimeit: Decorator to measure execution time of functions.
- pyGTSingleton: Singleton pattern decorator.
- pyGTIsType: Type checking decorator.
- pyGTRetry: Retry mechanism decorator.

Modules Imported:
- lru_cache from .cache
- ensure_method_exists from .class_method_checked
- contextmanager from .context_manager
- log_calls from .log_calls
- memoize from .memoization
- timeit from .timeit
- singleton from .singleton
- is_type from .type_checked
- retry from .retry

__all__:
- List of public objects of this module, as interpreted by import *.
"""
from .cache import lru_cache
from .class_method_checked import ensure_method_exists
from .context_manager import contextmanager
from .log_calls import log_calls
from .memoization import memoize
from .timeit import timeit
from .singleton import singleton
from .type_checked import is_type
from .retry import retry

__all__= [
    'pyGTCache',
    'pyGTEnsureMethodExists',
    'pyGTContextManager',
    'pyGTLogCalls',
    'pyGTMemoize',
    'pyGTTimeit',
    'pyGTSingleton',
    'pyGTIsType',
    'pyGTRetry'
]

pyGTCache = lru_cache
pyGTEnsureMethodExists = ensure_method_exists
pyGTContextManager = contextmanager
pyGTLogCalls = log_calls
pyGTMemoize = memoize
pyGTTimeit = timeit
pyGTSingleton = singleton
pyGTIsType = is_type
pyGTRetry = retry
