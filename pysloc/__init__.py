# pySloc/__init__.py

from abc import ABCMeta, abstractmethod, abstractproperty
import binascii, hashlib, os, re
from stat import *

__all__ = [ '__version__',      '__version_date__',
            'countLinesInDir',  'countLinesInPyFile', 'countLinesInSnoFile',
            # classes
            'Q',
          ]

# exported constants ------------------------------------------------
__version__      = '0.4.0'
__version_date__ = '2015-04-03'


# private constants -------------------------------------------------
TQUOTE = '"""'

# class(es) ---------------------------------------------------------
class Q(object):

    def __init__(self):

        # guesses language from file extension
        self._ext2lang = {
            'java'      : 'java',
            'go'        : 'golang',
            'py'        : 'python',
            'sno'       : 'snobol4',
        }
        # maps abbreviation to language name
        self._langMap = {
            'java'      : 'java',
            'go'        : 'golang',
            'py'        : 'python',
            'sno'       : 'snobol4',
        }

        self._notCodeFiles = {
            'COPYING',
            'README',
        }

    def ext2lang(self, s):
        if s in _ext2lang:
            return self._ext2lang[s]
        else:
            return None

    def langMap(self, s):
        if s in _langMap:
            return self._langMap[s]
        else:
            return None

    def notCodeFile(self, s):
        return s in self._notCodeFiles

# functions ---------------------------------------------------------
def countLinesInSnoFile(pathToFile, options):
    """ 
    already is a set containing hashes of files already counted 
    """

    linesSoFar, slocSoFar = (0,0)
    try:
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
                if lines[-1] == '':
                    lines = lines[:-1]
                for line in lines:
                    linesSoFar += 1
                    line = line.rstrip()
                    if len(line) > 0 and (line[0] != '*'):
                        slocSoFar += 1
            if options.verbose:
                print ("%-54s: %5d lines, %5d sloc" % (
                        pathToFile, linesSoFar, slocSoFar))
            options.already.add(h)
    except Exception as e:
        print("error reading '%s', skipping: %s" % (pathToFile, e))
    return linesSoFar, slocSoFar

def countLinesInPyFile(pathToFile, options):

    inTripleQuote         = False
    linesSoFar, slocSoFar = (0,0)
    try:
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
                if lines[-1] == '':
                    lines = lines[:-1]

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
        if options.verbose:
            print ("%-54s: %5d lines, %5d sloc" % (
                    pathToFile, linesSoFar, slocSoFar))
    except Exception as e:
        print("error reading '%s', skipping: %s" % (pathToFile, e))
    return (linesSoFar, slocSoFar)


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
                if name.endswith('.py'):
                    moreLines, moreSloc = countLinesInPyFile(pathToFile, options)
                    lines += moreLines
                    sloc  += moreSloc
                if name.endswith('.sno'):
                    moreLines, moreSloc = countLinesInSnoFile(pathToFile, options)
                    lines += moreLines
                    sloc  += moreSloc
    return lines, sloc
