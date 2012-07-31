#!/usr/bin/python2

import re

def getScan():
    """
    Return an object with the scanner corresponding
    to this module.
    """
    return InheritanceScan()


class InheritanceScan:
    """
    Scanner that will detect the inheritance in a python files
    and return edges of the corresponding graph.
    """

    def __init__(self):
        """
        Defines list of edges and the regex that will detect the import directives.
        -> edges have the corresponding format :  (obj, base, info)
        """
        self.edges = []
        mod = '[a-zA-Z, _\.-]+'
        inheritPattern = 'class[ ]+(?P<obj>%s)\((?P<base>%s)\):' % (mod, mod)
        self.inheritPattern = re.compile(inheritPattern)

    def getEdges(self):
        return self.edges

    def beginFile(self, fileName):
        self.edges = []

    def scanFile(self, f):
        for m in self.inheritPattern.finditer(f.read()):
            self.edges.append((m.group('obj'), m.group('base'), ''))
