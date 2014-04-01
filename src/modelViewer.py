#!/usr/bin/python2
#-*-coding:Utf-8 -*

from os.path import normpath
import os
import sys
import fnmatch

class modelViewer():
    """
    I am an object that aims to parse files and detect their model
    directive so as to create a dot file that contains a graph of
    this dependencies.
    The graph is written in the dot format in the file 'output.dot'
    I may be called several times, and the results will be added in the
    same dot file.
    """

    def __init__(self, validExt, dotName, scanner):
        """
        Init the modelViewer with the good scanner,
        colors, dot file, etc.
        """
        self.basepath = None
        self.scanner = scanner
        self.ext = validExt
        self.dot = open(dotName, 'w')
        self.colors = ['black', 'blue', 'red', 'gray',\
                       'green', 'yellow', 'turquoise', 'sienna']

        # Manage colors
        self.currentCol = 0
        self.nextCol = 0
        self.dirCol = {}
        self.fileCount = -1

        # init dot file
        self.dotHeader()


    def __call__(self, path):
        """
        Parse files and subdirectories from the @path given
        as argument. Result will be added in the dot file.
        """
        self.basepath = normpath(path)
        print(self.basepath)
        current = os.getcwd()
        os.chdir(path)
        self.setColor(os.getcwd())
        self.parse()
        os.chdir(current)


    def __del__(self):
        """
        End and close the @dot file.
        """
        self.dot.write("}")
        self.dot.close()


    def setColor(self, f):
        """
        Given a directory @f, determines the currentColor
        of the edges to be added in the graph.
        """
        if f in self.dirCol:
            self.currentCol = self.dirCol[f]
        else:
            if self.fileCount == 0:
                self.nextCol -= 1
            self.currentCol = self.nextCol
            self.dirCol[f] = self.nextCol
            self.nextCol += 1
            self.fileCount = 0


    def parse(self):
        """
        Recurcively list the content of directories from the current
        location and parse files that respect the good extensions.
        """
        
        for f in os.listdir(os.getcwd()):
            if os.path.isdir(f):
                os.chdir(f)
                self.setColor(os.getcwd())
                self.parse()
                os.chdir('../')
                self.setColor(os.getcwd())
            else:
                for ext in self.ext:
                    if fnmatch.fnmatch(f, ext):
                        self.fileCount += 1
                        self.parseFile(f, os.getcwd())



    def parseFile(self, filePath, dirpath):
        """
        Parse the file @filePath using the current scanner.
        Write the edges to the dot file.
        """
        self.scanner.beginFile(filePath, self.basepath, dirpath)

        # Parse file
        with open(filePath, 'r') as f:
            self.scanner.scanFile(f, dirpath, self.basepath)

        for u, v, info in self.scanner.getEdges():
            self.dotAddEdge(u, v, info)


    def dotAddEdge(self, u, v, info):
        """
        Add one edge between @u and @v in the dot file.
        The edge will have the label @info and the color
        @color
        """
        self.dot.write("\"%s\"->\"%s\"" % (u, v))
        self.dot.write("[color=\"%s\", label=\"%s\"]" % \
                (self.colors[self.currentCol % len(self.colors)], info))


    def dotHeader(self):
        """
        Write the dot header in the file @dot
        """
        options = ["digraph D {",
                   "  rankdir=LR",
                   "  ratio=\"fill\"",
                   "  node[shape=\"circle\"]"]
        self.dot.write("\n".join(options))

def usage():
    print('Usage of ./modelViewer :')
    print('./modelViewer Scanner [path [path ..]]')
    print('Scanner could be importScan or inheritanceScan.')


def main():
    """ Main Entry Point """
    if len(sys.argv) < 2:
        usage()
    else:
        v = modelViewer(['*.py'], 'output.dot', __import__(sys.argv[1]).getScan())
        if len(sys.argv) >= 3:
            for x in sys.argv[2::]:
                v(x)
        else:
            v('./')


if __name__ == '__main__':
    main()
