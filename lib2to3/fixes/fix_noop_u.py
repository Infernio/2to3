"""Changes code of the form u'' r'...' to simply r'...'."""

from ..pgen2 import token
from .. import fixer_base

class FixNoopU(fixer_base.BaseFix):
    BM_compatible = True
    run_order = 4 # run before unicode_literals fixer

    PATTERN = "STRING"

    def transform(self, node, results):
        # 1. The node in question must be of the form u''
        if node.value == 'u\'\'':
            siblings = node.parent.children
            my_index = siblings.index(node)
            # 2. It must have a sibling right after it
            next_index = my_index + 1
            if next_index < len(siblings):
                next_node = siblings[next_index]
                # 3. That sibling must be a string too
                if (next_node.type == token.STRING and
                    next_node.value[0] == u'r'):
                    # If all that is true, delete the u'' node
                    siblings[my_index].remove()
