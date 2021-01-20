"""Fixer that removes some obsolete WB classes."""

from .. import fixer_base

_obsolete = {'OrderedDefaultDict', 'UnicodeImporter'}

class FixWbOldClasses(fixer_base.BaseFix):
    BM_compatible = True
    PATTERN = "classdef< 'class' (%s) any+ >" % u' | '.join(
        "'%s'" % o for o in _obsolete)

    def transform(self, node, results):
        # Drop the entire class
        node.remove()
