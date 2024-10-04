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

from .baseTypes import *
from .Const import Const
__all__ = [
    'void',
    'ptr',
    'const'
    'u8',
    'u16',
    'u32',
    'i8',
    'i16',
    'i32',
    'i64',
    'char',
    'string',
    'boolean',
    'f2', 
    'f4', 
    'f8', 
    'f16', 
    'f32', 
    'f64',
    
]

void = Void
ptr = Pointer
const = Const
u8 = UInt8
u16 = UInt16
u32 = UInt32
u64 = UInt64
i8 = Int8
i16 = Int16
i32 = Int32
i64 = Int64
char = Char
string = String
NULL = NULL()
nullptr = nullptr()
boolean = Bool
f2 = Float2
f4 = Float4
f8 = Float8
f16 = Float16
f32 = Float32
f64 = Float64
