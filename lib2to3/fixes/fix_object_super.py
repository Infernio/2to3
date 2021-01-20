"""Remove redundant object superclass in class definitions."""

from .. import fixer_base

class FixObjectSuper(fixer_base.BaseFix):
    BM_compatible = True
    PATTERN = "classdef< 'class' any l_paren='(' super_obj='object' " \
              "r_paren=')' ':' any* >"

    def transform(self, node, results):
        # Simply drop the entire construct
        for target in ('l_paren', 'super_obj', 'r_paren'):
            results[target].remove()
