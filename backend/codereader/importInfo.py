import ast
from collections import namedtuple

class ImportCollector():
    def __init__(self):
        self.imports = namedtuple("Import", ["module", "name", "alias"])
        self.impCalls=[]
        
    def get_imports(self,root):
        for node in ast.iter_child_nodes(root):
            if isinstance(node, ast.Import):
#                print(dir(node.names))
                module = []
            elif isinstance(node, ast.ImportFrom):  
                module = node.module.split('.')
            else:
                continue

            for n in node.names:
                function=n.name.split('.')
                if module == [] and len(n.name.split('.')) >1:
                    module=n.name.split('.')[:-1]
                    function=n.name.split('.')[-1]
                elif (module == []):
                    module=n.name.split('.')
                    function=[]
                self.impCalls += [self.imports(module, function, n.asname)]
                module=[]
