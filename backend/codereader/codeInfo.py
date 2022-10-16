## @package MLigther
#    Copyright 2022 Hector D. Menendez
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#  
#  Documentation for this module.
#
#  More details.
import ast

class CallCollector(ast.NodeVisitor):
    def __init__(self):
        self.calls = []
        self.current = None

    def visit_Call(self, node):
        # new call, trace the function expression
        self.current = ''
        for child in node.args:
            if(isinstance(child,ast.Call)):
                oldcurrent=self.current
                self.current = None
                self.visit(child)
                self.current = oldcurrent
        self.visit(node.func)
        self.calls.append(self.current)
#        print(self.current)
#        print(type(self.current))
        self.current = None

    def generic_visit(self, node):
        if self.current is not None:
            print("warning: {} node in function expression not supported".format(node.__class__.__name__))
        super(CallCollector, self).generic_visit(node)

    # record the func expression 
    def visit_Name(self, node):
        if self.current is None:
            return
        self.current += node.id

    def visit_Attribute(self, node):
        if self.current is None:
            self.generic_visit(node)
        self.visit(node.value)
        if(self.current is None):
            return
        if(not node.attr is None): 
            self.current += '.' + node.attr


#tree = ast.parse('''\
#import numpy as np
#
#def foo():
#    if(np.random.rand(4) + np.random.randn(4) >2):
#      print("Hello")
#    print(linalg.norm(np.random.rand(4)))
#
#def foo2():
#    if(np.random.rand(4) + np.random.randn(4) >2):
#      print("Hello")
#    print(linalg.norm(np.random.rand(4)))
#''')
#cc = CallCollector()
#cc.visit(tree)
#print(cc.calls)
