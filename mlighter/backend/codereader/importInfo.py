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
from collections import namedtuple


class ImportCollector:
    def __init__(self):
        self.imports = namedtuple("Import", ["module", "name", "alias"])
        self.impCalls = []

    def get_imports(self, root):
        for node in ast.iter_child_nodes(root):
            if isinstance(node, ast.Import):
                #                print(dir(node.names))
                module = []
            elif isinstance(node, ast.ImportFrom):
                module = node.module.split(".")
            else:
                continue

            for n in node.names:
                function = n.name.split(".")
                if module == [] and len(n.name.split(".")) > 1:
                    module = n.name.split(".")[:-1]
                    function = n.name.split(".")[-1]
                elif module == []:
                    module = n.name.split(".")
                    function = []
                self.impCalls += [self.imports(module, function, n.asname)]
                module = []
