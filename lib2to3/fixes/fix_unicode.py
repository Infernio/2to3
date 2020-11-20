r"""Fixer for unicode.

* Changes unicode to str and unichr to chr.
"""

from ..pgen2 import token
from .. import fixer_base

_mapping = {"unichr" : "chr", "unicode" : "str"}

class FixUnicode(fixer_base.BaseFix):
    BM_compatible = True
    PATTERN = "'unicode' | 'unichr'"

    def transform(self, node, results):
        if node.type == token.NAME:
            new = node.clone()
            new.value = _mapping[node.value]
            return new
