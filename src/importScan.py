#!/usr/bin/python2

import re


def getScan():
    """
    Return an object with the scanner corresponding
    to this module.
    """
    return ImportScan()


class ImportScan:
    """
    Scanner that will detect the import directives in a python files
    and return edges of the corresponding graph.
    """

    def __init__(self):
        """
        Defines list of edges and the regex that will detect the import directives.
        -> edges have the corresponding format :  (obj, base, info)
        """
        self.edges = []
        mod = '[a-zA-Z, _-]+'
        simpleImport = 'import[ ]+(?P<mod1>%s)' % (mod)
        fromImport = 'from[ ]+(?P<mod2>%s)[ ]+import[ ]+(?P<info>%s)' % (mod, mod)
        functionImport = '__import__[(\'"]{2}(?P<mod3>%s)[)\'"]{2}' % (mod)
        importPattern = '%s|%s|%s' % (functionImport, fromImport, simpleImport)
        self.importPattern = re.compile(importPattern)

    def getEdges(self):
        return self.edges

    def beginFile(self, fileName):
        self.prefix = fileName.split('.')[0]
        self.edges = []

    def scanFile(self, f):
        for m in self.importPattern.finditer(f.read()):
            info = ''
            if m.group('info'):
                info = m.group('info')
            if m.group('mod1'):
                for imp in m.group('mod1').split(','):
                    self.edges.append((self.prefix, imp, info))
            elif m.group('mod2'):
                self.edges.append((self.prefix, m.group('mod2'), info))
            elif m.group('mod3'):
                self.edges.append((self.prefix, m.group('mod3'), info))
