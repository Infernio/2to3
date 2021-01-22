"""Fixes certain APIs that were changed. I ensured this will have no false
positives in WB's codebase."""

from ..pgen2 import token
from .. import fixer_base

_remaps = {'getheaders': 'get', 'clock': 'process_time'}

class FixWbRenames(fixer_base.BaseFix):
    BM_compatible = True
    PATTERN = "'getheaders'"

    def transform(self, node, results):
        if node.type == token.NAME:
            new = node.clone()
            new.value = _remaps[node.value]
            return new
