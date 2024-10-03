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
from .command import Command
from .factory import CallbackFactory
from .functor import F
from .mediator import Mediator
from .meta import Meta
from .observer import Observer, Subject
from .singleton import Singleton
from .smart_ptr import SmartPointer
from .time_ptr import TimeitPtr
from .visitor import Visitor


__all__ = [
    'pyGTCommand',
    'pyGTCallback',
    'pyGTFunctor',
    'pyGTSingleton',
    'pyGTSmartPointer',
    'pyGTTimeitPtr',
    'pyGTVisitor',
    'pyGTMediator',
    'pyGTMeta',
    'pyGTSubject',
    'pyGTObserver',
]


pyGTCommand = Command
pyGTCallback = CallbackFactory
pyGTFunctor = F
pyGTSingleton = Singleton
pyGTSmartPointer = SmartPointer
pyGTTimeitPtr = TimeitPtr
pyGTVisitor = Visitor
pyGTMediator = Mediator
pyGTMeta = Meta
pyGTSubject = Subject
pyGTObserver = Observer