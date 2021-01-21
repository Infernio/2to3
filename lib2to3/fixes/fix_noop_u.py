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
            next_node = node.next_sibling
            # 2. It must have a sibling right after it
            if next_node:
                # 3. That sibling must be a string too
                if (next_node.type == token.STRING and
                    next_node.value[0] == 'r'):
                    # If all that is true, delete the u'' node
                    node.remove()
                    # Move the other node into the position this one was in
                    # (this drops e.g. spaces between the two nodes)
                    next_node.prefix = node.prefix
