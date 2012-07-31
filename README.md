PyProjectViewer
===============

## Introduction

PyProjectViewer provides a simple script able to build graph
from your python project. The graph could be the import one,
or the inheritance one.

## Requirements

You need Python to use this script. Versions 3.x and 2.x are supported.

## Getting Started

* import graph : ./modelViewer.py importScan
* inheritance graph : ./modelViewer.py inheritanceScan

This will generate a dot file (output.dot). You can generate a postscript file
from the dot file with the following command :

* dot output.dot -Tps -o output.ps
