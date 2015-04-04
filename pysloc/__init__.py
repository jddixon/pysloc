# pySloc/__init__.py

from abc import ABCMeta, abstractmethod, abstractproperty
import binascii, hashlib, os, re
from stat import *

__all__ = [ '__version__',      '__version_date__',
            'countLinesInDir',  'countLinesInGenericFile',
            'countLinesInPyFile', 'countLinesInSnoFile',
            # classes
            'Q',
          ]

# exported constants ------------------------------------------------
__version__      = '0.4.1'
__version_date__ = '2015-04-04'


# private constants -------------------------------------------------
TQUOTE = '"""'

# class(es) ---------------------------------------------------------
class Q(object):

    __all__ = ['ext2lang','langMap','notCodeFile', '_notCodeFiles',
            ]
    def __init__(self):

        self._ext2Counter = {
            'py'        : countLinesInPyFile,
            'sno'       : countLinesInSnoFile,
        }
        # guesses language short name from file extension
        self._ext2Lang  = {
            'go'        : 'go',
            'html'      : 'html',
            'java'      : 'java',
            'md'        : 'md',
            'py'        : 'py',
            'sh'        : 'sh',
            'sno'       : 'sno',
        }
        # maps abbreviation to language name
        self._langMap = {
            'gen'       : 'generic',
            'go'        : 'golang',
            'html'      : 'html',
            'java'      : 'java',
            'md'        : 'markdown',
            'py'        : 'python',
            'sno'       : 'snobol4',
        }

        # a set of extensions known not to be source code 
        self._notCodeExt = {
            # 'dat',    # arguable
            'jar',
            'pyc',
        }
        # a set of file and directory names known not to contain source code
        self._notCodeFiles = {
            '__pycache__',
            'AUTHORS',
            'CONTRIBUTORS',
            'COPYING', 'COPYING.AUTOCONF.EXCEPTION', 
            'COPYING.GNUBL', 'COPYING.LIB',
            'LICENSE',
            'NEWS',
            'PATENTS',
            'README',
            'TODO',
        }

    def ext2Counter(self, s):
        if s in self._ext2Counter:
            return self._ext2Counter[s]
        else:
            return None

    def ext2lang(self, s):
        """ Given a file name extension, return the longer language name """
        if s in _ext2lang:
            return self._ext2lang[s]
        else:
            return None

    def langMap(self, s):
        """ Given a short file name, return the longer language name """
        if s in _langMap:
            return self._langMap[s]
        else:
            return None

    def notCodeFile(self, s):
        return s in self._notCodeFiles

# functions =========================================================

# DIR-LEVEL COUNTER(S) ----------------------------------------------
def countLinesInDir(pathToDir, options):
    ## DEBUG
    #print("DIRECTORY %s" % pathToDir)
    #if not options:
    #    print("  NIL OPTIONS")
    #else:
    #    for pair in options._get_kwargs():
    #        ls = pair[0]
    #        rs = pair[1]
    #        print("%s => %s" % (ls, rs))
    ## END
    lines, sloc = (0,0)
    files = os.listdir(pathToDir)
    if files:
        q = Q()
        for name in sorted(files):
            # consider exclusions ...
            if options.exRE is not None and options.exRE.search(file) is not None:
                continue
            pathToFile = os.path.join(pathToDir, name)
            s = os.lstat(pathToFile)        # ignores symlinks
            mode = s.st_mode
            if S_ISDIR(mode):
                (moreLines, moreSloc) = countLinesInDir(pathToFile, options)
                lines += moreLines
                sloc  += moreSloc
            elif S_ISREG(mode):
                if q.notCodeFile(name):
                    pass
                else:
                    counted = False
                    a, b, ext = name.rpartition('.')
                    if b == '.':
                        counter = q.ext2Counter(ext)
                        if counter:
                            moreLines, moreSloc = counter(pathToFile, options)
                            lines += moreLines
                            sloc  += moreSloc
                            counted = True
                    
                    if not counted and options.verbose:
                        print("Don't know how to count lines in %s" % name)

    return lines, sloc

# FILE-LEVEL COUNTERS -----------------------------------------------

def checkWhetherAlreadyCounted(pathToFile, options):
    """
    Given a text file, try to split it into a list of lines.  May raise
    an exception.  If the file has been seen before, will return an 
    empty list of lines.  Otherwise it retuns the list of lines and the
    file's hash.
    
    options.already is a set containing hashes of files already counted 
    """
    lines, h = None, None
    with open(pathToFile, 'rb') as f:
        data = f.read()
    if data and (len(data)>0):
        d = hashlib.sha1()
        d.update(data)
        h = d.hexdigest()   # a string
        # XXX This is very messy; should distinguish levels of 
        # verbosity and only print this if more verbose
        #if options.verbose:
        #    print("    %s <-- %s" % (h, pathToFile))
        if h in options.already:
            if options.verbose:
                print("skipping %s, already counted" % pathToFile)
        else:
            try:
                decoded = data.decode('utf-8')
            except Exception:
                decoded = data.decode('latin-1')
            lines = decoded.split("\n")

            # drop spurious last line caused by terminating newline
            if lines and len(lines) > 1:
                if lines[-1] == '':
                    lines = lines[:-1]
    return lines, h

def countLinesInGenericFile(pathToFile, options):
    """ 
    Count lines in a file where the sharp sign ('#') is the comment
    marker.  That is, we ignore blank lines, lines consisting solely of 
    spaces, and those starting with zero or more spaces followed by
    a sharp sign.
    """

    linesSoFar, slocSoFar = (0,0)
    try:
        lines, hash = checkWhetherAlreadyCounted(pathToFile, options)
        if (hash != None) and (lines != None):
            for line in lines:
                linesSoFar += 1
                # This could be made more efficient.
                line = line.strip()
                if len(line) > 0 and (line[0] != '#'):
                    slocSoFar += 1
            options.already.add(hash)
            if options.verbose:
                print ("%-54s: %5d lines, %5d sloc" % (
                        pathToFile, linesSoFar, slocSoFar))
    except Exception as e:
        print("error reading '%s', skipping: %s" % (pathToFile, e))
    return linesSoFar, slocSoFar

def countLinesInPyFile(pathToFile, options):

    inTripleQuote         = False
    linesSoFar, slocSoFar = (0,0)
    try:
        lines, hash = checkWhetherAlreadyCounted(pathToFile, options)
        if (lines != None) and (hash != None):
            for line in lines:
                if inTripleQuote:
                    # we always count this line
                    linesSoFar += 1
                    slocSoFar  += 1
                    count = line.count(TQUOTE)
                    if count % 2 :
                        inTripleQuote = False
                else:
                    linesSoFar += 1
                    s = line.partition('#')[0]  # strip off comments
                    line = s.strip()            # strip leading & trailing
                    if line != '':
                        slocSoFar += 1
                    count = line.count(TQUOTE)
                    if count % 2:
                        inTripleQuote = True
            options.already.add(hash)
            if options.verbose:
                print ("%-54s: %5d lines, %5d sloc" % (
                    pathToFile, linesSoFar, slocSoFar))
    except Exception as e:
        print("error reading '%s', skipping: %s" % (pathToFile, e))
    return (linesSoFar, slocSoFar)


def countLinesInSnoFile(pathToFile, options):
    """ 
    already is a set containing hashes of files already counted 
    """

    linesSoFar, slocSoFar = (0,0)
    try:
        lines, hash = checkWhetherAlreadyCounted(pathToFile, options)
        if (hash != None) and (lines != None):
            for line in lines:
                linesSoFar += 1
                line = line.rstrip()
                if len(line) > 0 and (line[0] != '*'):
                    slocSoFar += 1
            options.already.add(hash)
            if options.verbose:
                print ("%-54s: %5d lines, %5d sloc" % (
                        pathToFile, linesSoFar, slocSoFar))
    except Exception as e:
        print("error reading '%s', skipping: %s" % (pathToFile, e))
    return linesSoFar, slocSoFar

