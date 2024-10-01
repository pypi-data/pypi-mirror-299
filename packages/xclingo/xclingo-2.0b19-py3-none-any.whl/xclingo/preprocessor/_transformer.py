from clingo.ast import Transformer

from pdb import set_trace

"""
Handles the renaming of anonymous '_' variables.
"""
class AnonVariableRenamer(Transformer):
    _anon_id = -1

    def visit_Variable(self, node):
        if node.name == '_':
            self._anon_id+=1
            return node.update(name=f'{node.name}XclingoAnon{str(self._anon_id)}')
        else:
            return node