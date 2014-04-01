#!/usr/bin/python2

from os.path import normpath, join
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
        -> edges have the corresponding format :  (obj, base, imported)
        """
        self.edges = []
        mod = '[.\w,_ ()-]+'
        simpleImport = r"import[\s]+(?P<mod1>[-._\w]+)" # import name
        fromImport = r"""
            from[\s]+
            (?P<mod2>[-._\w]+)
            [\s]+
            import
            [\s(]+
            (?P<imported>.+)[\s)]*"""
        functionImport = r'__import__[(\'"]{2}(?P<mod3>%s)[)\'"]{2}' % (mod)
        importPattern = '%s|%s|%s' % (functionImport, fromImport, simpleImport)
        self.importPattern = re.compile(importPattern, re.VERBOSE)

    def getEdges(self):
        return self.edges

    def beginFile(self, fileName, base, dirpath):
        self.prefix = _norm_module(base, dirpath, '.' + fileName.split('.')[0])
        self.edges = []

    def scanFile(self, f, dirpath, base, stdfilter=True):
        for m in self.importPattern.finditer(f.read()):
            imported = ''
            if m.group('imported'):
                imported = m.group('imported')
            mod = None
            if m.group('mod1'):
                mod = m.group('mod1')
            if m.group('mod2'):
                mod = m.group('mod2')
            if m.group('mod3'):
                mod = m.group('mod3')

            if mod is not None:
                mod = _norm_module(base, dirpath, mod)
                if (not stdfilter) or (mod not in std_modules):
                    self.edges.append((self.prefix, mod, imported))


def _norm_module(base, dirpath, path):
    new_path = []
    # Relative path
    if path[0] == '.':
        new_path.append(dirpath)
        for i, char in enumerate(path[1:]):
            if char == '.':
                new_path.append('..')
            else:
                path = path[i + 1:]
                break

    # Split with '.'
    modules = path.split('.')
    if len(modules) > 1 or len(new_path) > 0:
        if len(new_path) == 0:
            new_path.append(dirpath)
        # Import a relative module
        new_path.extend(modules)
    elif path in std_modules:
        # Import a stdlib module
        return path
    else:
        # Import a local module
        new_path = [dirpath, path]

    mod = normpath(join(*new_path))
    if mod.startswith(base):
        mod = mod[len(base) + 1:]
    return mod


std_modules = [
    "__future__",
    "__main__",
    "_dummy_thread",
    "_thread",
	"abc",
	"aifc",
	"argparse",
	"array",
	"ast",
	"asynchat",
	"asyncio",
	"asyncore",
	"atexit",
	"audioop",
	"base",
	"bdb",
	"binascii",
	"binhex",
	"bisect",
	"builtins",
	"bz",
	"calendar",
	"cgi",
	"cgitb",
	"chunk",
	"cmath",
	"cmd",
	"code",
	"codecs",
	"codeop",
	"collections",
	"colorsys",
	"compileall",
	"concurrent",
	"configparser",
	"contextlib",
	"copy",
	"copyreg",
	"cProfile",
	"crypt",
	"csv",
	"ctypes",
	"curses",
	"datetime",
	"dbm",
	"decimal",
	"difflib",
	"dis",
	"distutils",
	"doctest",
	"dummy",
	"email",
	"encodings",
	"ensurepip",
	"enum",
	"errno",
	"faulthandler",
	"fcntl",
	"filecmp",
	"fileinput",
	"fnmatch",
	"formatter",
	"fpectl",
	"fractions",
	"ftplib",
	"functools",
	"gc",
	"getopt",
	"getpass",
	"gettext",
	"glob",
	"grp",
	"gzip",
	"hashlib",
	"heapq",
	"hmac",
	"html",
	"http",
	"imaplib",
	"imghdr",
	"imp",
	"importlib",
	"inspect",
	"io",
	"ipaddress",
	"itertools",
	"json",
	"keyword",
	"lib",
	"linecache",
	"locale",
	"logging",
	"lzma",
	"macpath",
	"mailbox",
	"mailcap",
	"marshal",
	"math",
	"mimetypes",
	"mmap",
	"modulefinder",
	"msilib",
	"msvcrt",
	"multiprocessing",
	"netrc",
	"nis",
	"nntplib",
	"numbers",
	"operator",
	"optparse",
	"os",
	"ossaudiodev",
	"parser",
	"pathlib",
	"pdb",
	"pickle",
	"pickletools",
	"pipes",
	"pkgutil",
	"platform",
	"plistlib",
	"poplib",
	"posix",
	"pprint",
	"profile",
	"pstats",
	"pty",
	"pwd",
	"py",
	"pyclbr",
	"pydoc",
	"queue",
	"quopri",
	"random",
	"re",
	"readline",
	"reprlib",
	"resource",
	"rlcompleter",
	"runpy",
	"sched",
	"select",
	"selectors",
	"shelve",
	"shlex",
	"shutil",
	"signal",
	"site",
	"smtpd",
	"smtplib",
	"sndhdr",
	"socket",
	"socketserver",
	"spwd",
	"sqlite",
	"ssl",
	"stat",
	"statistics",
	"string",
	"stringprep",
	"struct",
	"subprocess",
	"sunau",
	"symbol",
	"symtable",
	"sys",
	"sysconfig",
	"syslog",
	"tabnanny",
	"tarfile",
	"telnetlib",
	"tempfile",
	"termios",
	"test",
	"textwrap",
	"threading",
	"time",
	"timeit",
	"token",
	"tokenize",
	"trace",
	"traceback",
	"tracemalloc",
	"tty",
	"turtle",
	"types",
	"unicodedata",
	"unittest",
	"urllib",
	"uu",
	"uuid",
	"venv",
	"warnings",
	"wave",
	"weakref",
	"webbrowser",
	"winreg",
	"winsound",
	"xdrlib",
	"zipfile",
	"zipimport",
	"zlib"
]
