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
This module defines the Visitor and Element classes for implementing the Visitor design pattern
to traverse and manipulate Abstract Syntax Tree (AST) elements.

Classes:
    Visitor: A base class for creating visitors that can traverse AST elements.
    Element: A base class for AST elements that can be visited by a Visitor.

Usage example:
    class MyElement(Element):
        def __init__(self, value):
            self.value = value


    class MyVisitor(Visitor):
        def visit_MyElement(self, element):
            return element.value * 2


    element = MyElement(10)
    visitor = MyVisitor()

    print(visitor.visit(element))  # Output: 20
"""
__all__ = ['Visitor', 'Element']


class Visitor(object):
    """
    This class is used to visit the AST elements
    """

    def visit(self, __element):
        """
        This method is used to visit the AST elements
        :param __element: element to be visited
        :return: None
        """
        method_name = 'visit_' + __element.__class__.__name__
        method = getattr(self, method_name, self.generic_visit)
        return method(__element)

    def generic_visit(self, __element):
        """
        This method is used to visit the AST elements
        :param __element:  element to be visited
        :return: None
        """
        raise NotImplementedError(f'No visit_{__element.__class__.__name__} method')


class Element(object):
    """
    This class is used to represent the elements of the AST tree and to be used by the Visitor class
    to visit the AST elements and to return the resultant AST tree after visiting the elements
    """

    def accept(self, __visitor):
        """
        This method is used to accept the visitor and to visit the AST elements
        :param __visitor: visitor to be used to visit the AST elements
        :return: None
        """
        return __visitor.visit(self)

