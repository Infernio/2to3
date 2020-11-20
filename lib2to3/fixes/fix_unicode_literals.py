r"""Fixer for unicode literals.

* If "...\u..." is not unicode literal change it into "...\\u...".

* Change u"..." into "...".
"""

from ..pgen2 import token
from .. import fixer_base

class FixUnicode(fixer_base.BaseFix):
    BM_compatible = True
    PATTERN = "STRING"

    def start_tree(self, tree, filename):
        super(FixUnicode, self).start_tree(tree, filename)
        self.unicode_literals = 'unicode_literals' in tree.future_features

    def transform(self, node, results):
        if node.type == token.STRING:
            val = node.value
            if not self.unicode_literals and val[0] in '\'"' and '\\' in val:
                val = r'\\'.join([
                    v.replace('\\u', r'\\u').replace('\\U', r'\\U')
                    for v in val.split(r'\\')
                ])
            if val[0] in 'uU':
                val = val[1:]
            if val == node.value:
                return node
            new = node.clone()
            new.value = val
            return new
