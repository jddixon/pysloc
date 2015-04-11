# pySloc/__init__.py

from abc import ABCMeta, abstractmethod, abstractproperty
import binascii, hashlib, os, re
from stat import *

__all__ = [ '__version__',      '__version_date__',
            'countLinesInDir',
            'countLinesC',      'countLinesGeneric',
            'countLinesGo',     'countLinesJava',   'countLinesOcaml',
            'countLinesPython', 'countLinesRuby',   'countLinesSnobol',
            # classes
            'K', 'Q',
          ]

# exported constants ------------------------------------------------
__version__      = '0.4.8'
__version_date__ = '2015-04-11'


# private constants -------------------------------------------------
TQUOTE = '"""'

# class(es) ---------------------------------------------------------
class K(object):
    """ a holder for various counts """

    LOC   = 0   # lines of non-test code
    SLOC  = 1   # of which source lines
    TLOC  = 2   # lines of test code
    TSLOC = 3   # of which source lines

    def __init__(self):
        # we maintain a map from lang to a list of 4: lines, sloc, tlines, tsloc,
        # where t means test
        self.m = {}

    def foo(self):
        print("hi, I'm your neighborhood foo!")

    def addCounts(self, lang, l, s):
        """ add non-test line count and source line count for language"""

        # XXX we want l and s to be non-negative integers

        if not lang in self.m:
            self.m[lang] = [0,0,0,0]
        self.m[lang][K.LOC]  += l
        self.m[lang][K.SLOC] += s


    def addTestCounts(self, lang, l, s):
        """ add test line count and source line count for language"""

        # XXX we want l and s to be non-negative integers

        if not lang in self.m:
            self.m[lang] = [0,0,0,0]
        self.m[lang][K.TLOC]  += l
        self.m[lang][K.TSLOC] += s

    def getCounts(self, lang):
        if (not lang) or (not lang in self.m):
            return (0,0,0,0)
        else:
            return self.m[lang]

    def prettyCounts(self, lang):
        """
        Return a string containing the short name of the language and
        the total line count, the source line count, and the percentage
        of source lines which are test lines.  The total line count
        includes the source line count.  As an example a python file
        with 17 lines of which 12 are source, of which 9 are test code
        would produce the string 'py:17/12 T%75.0'

        """
        if (not lang) or (not lang in self.m):
            return '%s: 0' % lang
        else:
            l, s, tl, ts = self.m[lang]
            if ts > 0:
                return "%s:%d/%d T%.1f%%" % (lang, l+tl, s+ts, 100.0*ts/(s+ts))
            else:
                return "%s:%d/%d" % (lang, l+tl, s)

    def prettyBreakDown(self):
        """
        Generate a semicolon-separated list sorted by decreasing SLOC.
        """

        # flatten the list to make it easier to sort
        f = []
        for k,v in self.m.items():
            f.append([k] + v)
        results=[]
        for x in sorted(f, key=lambda fields: fields[K.SLOC+1], reverse=True):
            results.append( self.prettyCounts(x[0]) )
        print('; '.join(results))

    def getTotals(self):
        totalL, totalS, totalTL, totalTS = 0,0,0,0
        for lang in self.m:
            l, s, tl, ts = self.m[lang]
            totalL  += l    # lines of non-test code
            totalS  += s    # lines of which are source code
            totalTL += tl   # lines of test code
            totalTS += ts   # lines of which are source code
        return totalL, totalS, totalTL, totalTS

class Q(object):

    __all__ = ['ext2lang',
            'getCounter', 'getLongName',
            'langMap',
            'nonCodeExt','notCodeFile',
            ]
    def __init__(self):

        # Note Ocaml comments are (* ... *) but allow nesting.  File
        # extensions are .ml (source code) and .mli (header; and then
        # .cmo/.cmx, .cmi, .cma/.cmxa are compiled forms.

        # Maps short name to counter function; limit these to 4 characters.
        self._lang2Counter = {
            'asm'       : countLinesGeneric,        # s, S, asm
            'c'         : countLinesC,              # ansic
            'csh'       : countLinesGeneric,        # csh, tcsh
            'gen'       : countLinesGeneric,        # treat # as comment
            'go'        : countLinesGo,             # golang
            'java'      : countLinesJava,           # plain old Java
            'ml'        : countLinesOcaml,          # ocaml, tentative abbrev
            'py'        : countLinesPython,         # yes, Python
            'rb'        : countLinesRuby,           # ruby
            'sed'       : countLinesGeneric,        # stream editor
            'sh'        : countLinesGeneric,        # bash, sh
            'sno'       : countLinesSnobol,         # snobol4
            'tcl'       : countLinesGeneric,        # tcl, tk, itk
        }
        # Guesses language short name (abbrev) from file extension.
        # See sloccount's break_filelist for hints.
        # Note {pl,pm,perl,pl} => perl
        self._ext2Lang  = {
            'asm'       : 'asm',
            'bash'      : 'sh',
            'c'         : 'c',                      # ansi c
            'csh'       : 'csh',
            'go'        : 'go',                     # same counter as C, Java ?
            'h'         : 'c',                      # PRESUMED ANSI C
            'html'      : 'html',                   # no counter
            'itk'       : 'tcl',
            'java'      : 'java',
            'md'        : 'md',                     # no counter
            'ml'        : 'ml',                     # ocaml
            'mli'       : 'ml',                     # ocaml extension
            'py'        : 'py',
            'rb'        : 'rb',
            'S'         : 'asm',
            's'         : 'asm',
            'sed'       : 'sed',
            'sh'        : 'sh',
            'sno'       : 'sno',
            'tcsh'      : 'csh',
            'tcl'       : 'tcl',
            'tk'        : 'tcl',
        }
        # Maps lang short name (abbrev) to fuller language name.
        # By convention, short names are limited to 4 chars.
        self._langMap = {
            'asm'       : 'assembler',
            'c'         : 'ansic',
            'csh'       : 'csh',
            'gen'       : 'generic',
            'go'        : 'golang',
            'html'      : 'html',
            'java'      : 'java',
            'md'        : 'markdown',
            'ml'        : 'ocaml',
            'py'        : 'python',
            'rb'        : 'ruby',
            'sed'       : 'sed',
            'sh'        : 'shell',
            'sno'       : 'snobol4',
            'tcl'       : 'tcl',
        }

        # A set of extensions known NOT to be source code.
        self._nonCodeExts = {
            'a',                                    # library, linked object
            'cma', 'cmi', 'cmo', 'cmx', 'cmxa',     # ocaml compiled
            # 'dat',                                # arguable
            'gz',
            'jar',
            'md',                                   # markdown
            'o',                                    # object
            'pyc',
            'so',
            'svn-base',
            'swp',                                  # vi/vim temporary file
            'zip',
        }
        # A set of file and directory names known NOT to contain source code
        self._notCodeDirs = {
            '.git',
            '.svn',
            'ghpDoc',
        }
        # files which definitely do not contain source code
        self._notCodeFiles = {
            '.gitignore',
            '.wrapped',
            '__pycache__',
            'AUTHORS',
            'CHANGES', 'ChangeLog',
            'CONTRIBUTORS',
            'COPYING', 'COPYING.AUTOCONF.EXCEPTION',
                'COPYING.GNUBL', 'COPYING.LIB',
            'LICENSE',
            'MANIFEST',
            'NEWS',
            'PATENTS',
            'README',
            'TODO',
        }

    # public interface ==============================================

    def ext2Lang(self, s):
        if s in self._ext2Lang:
            return self._ext2Lang[s]
        else:
            return None

    def getCounter(self, lang, isCLIArg=False):
        """
        Enter with the language (abbrev) of a file and whether the name is on
        the command line.  If there is a counter matching that name, return a
        reference to it.  Otherwise, if this is a CLI argument, return the
        generic counter.  Otherwise, return None.

        XXX If the name on the command line is a directory name, should
        be handled differently.
        """
        if lang and (len(lang) > 0) and (lang in self._lang2Counter):
            return self._lang2Counter[lang]
        elif isCLIArg:
            return countLinesGeneric
        else:
            return None

    def getLongName(self, s):
        """ Given a short file name, return the longer language name """
        if s in self._langMap:
            return self._langMap[s]
        else:
            return None

    def nonCodeExt(self, s):
        return s in self._nonCodeExts

    def notCodeDir(self, s):
        return s in self._notCodeDirs

    def notCodeFile(self, s):
        return s in self._notCodeFiles

    def guessLang(self, fileName, isCLIArg = False, verbose=False):
        """
        Guess the short name of the language and whether it is a test file
        depending on whether the name appears on the command line (we
        always count any file named on the command line).
        """
        lang, isTest = None, False     # defaults
        if (fileName != None) and (fileName != '') :
            ext  = None
            if not self.notCodeFile(fileName):
                # get any extension
                a, b, c = fileName.rpartition('.')
                if b == '.':
                    # we have an extension
                    ext = c
                    if not self.nonCodeExt(ext):
                        # we have an extension and it's not prohibited
                        lang    = self.ext2Lang(ext)
                        if (lang == None) and isCLIArg:
                            lang = 'gen'
                elif isCLIArg:
                    lang = 'gen'

        if lang == 'go':
            isTest = fileName.endswith('_test.go')
        elif lang == 'py':
            isTest = fileName.startswith('test')

        # DEBUG
        if verbose > 1:
            if ext != None:
                print("  %s: find ext '%s', GUESS lang %s" % (fileName, ext, lang))
            else:
                print("  %s: NO ext, GUESS lang %s" % (fileName, lang))

        # END
        return lang, isTest

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
    k       = options.k
    q       = options.q
    verbose = options.verbose
    lines, sloc = (0,0)
    files = os.listdir(pathToDir)
    if files:
        q = options.q
        for name in sorted(files):
            # consider exclusions ...
            if options.exRE is not None and options.exRE.search(file) is not None:
                continue
            isTest = False  # default
            pathToFile = os.path.join(pathToDir, name)
            s = os.lstat(pathToFile)        # ignores symlinks
            mode = s.st_mode
            if S_ISDIR(mode):
                (moreLines, moreSloc) = countLinesInDir(pathToFile, options)
                lines += moreLines
                sloc  += moreSloc
            elif S_ISREG(mode):
                if q.notCodeFile(name):
                    if verbose > 1:
                        print("Not a code file: %s" % name)
                else:
                    # XXX Note command line argument may be relative or
                    # absolute path to file, terminated by base file name
                    # and extension.
                    counted = False
                    # isCLIArg == False
                    lang, isTest = q.guessLang(name,verbose=verbose)
                    if lang != None:
                        counter = q.getCounter(lang, True)
                        if counter:
                            moreLines, moreSloc = counter(
                                    pathToFile, options, lang)
                            lines += moreLines  # VESTIGIAL
                            sloc  += moreSloc

                            if isTest:
                                k.addTestCounts(lang, moreLines, moreSloc)
                            else:
                                k.addCounts(lang, moreLines, moreSloc)
                            counted = True

                    if not counted and options.verbose > 1:
                        print("    skipping %s" % name)

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
        if options.verbose > 1:
            print("    %s <-- %s" % (h, pathToFile))
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

def countLinesC(path, options, lang):
    l, s = 0,0
    if (not path.endswith('.pb-c.c')) and (not path.endswith('.pb-c.h')):
        l, s = countLinesJavaStyle(path, options, lang)
    return l, s

def countLinesGeneric(pathToFile, options, lang):
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
                print ("%-49s: %-4s %5d lines, %5d sloc" % (
                        pathToFile, lang, linesSoFar, slocSoFar))
    except Exception as e:
        print("error reading '%s', skipping: %s" % (pathToFile, e))
    return linesSoFar, slocSoFar

def countLinesGo(pathToFile, options, lang):
    linesSoFar,slocSoFar    = (0,0)
    if not pathToFile.endswith('.pb.go'):
        linesSoFar, slocSoFar = countLinesJavaStyle(pathToFile, options, lang)
    return linesSoFar, slocSoFar

def countLinesJava(pathToFile, options, lang):
    linesSoFar,slocSoFar    = (0,0)
    if not pathToFile.endswith('Protos.java'):
        linesSoFar, slocSoFar = countLinesJavaStyle(pathToFile, options, lang)
    return linesSoFar, slocSoFar

OLD_COMMENT_PAT = "^(.*)/\*.*\*/(.*)$"
OLD_COMMENT_RE  = re.compile(OLD_COMMENT_PAT)

def countLinesJavaStyle(pathToFile, options, lang):
    linesSoFar,slocSoFar    = (0,0)
    inMultiLine             = False
    try:
        lines, hash = checkWhetherAlreadyCounted(pathToFile, options)
        if (hash != None) and (lines != None):
            for line in lines:
                linesSoFar += 1

                #print "\nINITIALLY '%s'" % line.strip()

                if not inMultiLine:
                    m = OLD_COMMENT_RE.match(line)
                    if m:
                        line = m.group(1) + m.group(2)
                        # print "LINE AFTER OLD COMMENT DROPPED: %s" % line
                    s = line.partition('/*')
                    if s[1] == '/*':
                        line = s[0]
                        inMultiLine = True

                if inMultiLine:
                    s = line.partition('*/')
                    if s[1] == '*/':
                        line = s[2]
                        inMultiLine = False
                    else:
                        line = ''

                #print "AFTER MULTI_LINE TESTS: '%s'" % line.strip()
                if line is not None and line != '':
                    s = line.partition('//')[0]     # strip off comments
                    line = s.strip()                # strip off leading, trailing
                    if line != '':
                        slocSoFar += 1
                #print "AFTER COMMENT STRIPPING: '%s'" % line.strip()


            options.already.add(hash)
            if options.verbose:
                print ("%-49s: %-4s %5d lines, %5d sloc" % (
                    pathToFile, lang, linesSoFar, slocSoFar))

    # SHOULD BE OK:
    except Exception as e:
        print("error reading '%s', skipping: %s" % (pathToFile, e))
    return (linesSoFar, slocSoFar)

def countLinesOcaml(pathToFile, options, lang):
    """
    Count lines in an Ocaml file where comments are delimited by
    (* and *).  These may be nested.  We ignore blank lines and lines
    consisting solely of spaces and comments.
    """

    linesSoFar, slocSoFar = (0,0)
    try:
        lines, hash = checkWhetherAlreadyCounted(pathToFile, options)
        if (hash != None) and (lines != None):
            depth = 0                           # comment depth
            for line in lines:
                linesSoFar += 1
                nonSpaceSeen = False
                lParenSeen   = False            # might start (*
                starSeen     = False            # might start *)
                for ch in list(line):
                    # ignore other unicode space chars for now
                    if ch == ' ' or ch == '\t':
                        lParenSeen = False
                        starSeen   = False
                        continue
                    elif depth == 0:
                        if lParenSeen:
                            if ch == '*':
                                depth += 1
                            else:
                                nonSpaceSeen = True
                            lParenSeen = False
                        elif starSeen:
                            if ch==')':
                                if depth > 0:
                                    depth -= 1
                                else:
                                    nonSpaceSeen = True
                                starSeen = False
                            else:
                                nonSpaceSeen = True
                        elif ch == '(':
                            lParenSeen = True
                        elif ch == '*':
                            starSeen = True
                        else:
                            nonSpaceSeen = True
                    else:
                        # depth > 0
                        if lParenSeen:
                            if ch == '*':
                                depth += 1
                            lParenSeen = False
                        elif starSeen:
                            if ch==')':
                                if depth > 0:
                                    depth -= 1
                                starSeen = False
                        elif ch == '(':
                            lParenSeen = True
                        elif ch == '*':
                            starSeen = True

                if nonSpaceSeen:
                    slocSoFar += 1

            options.already.add(hash)
            if options.verbose:
                print ("%-49s: %-4s %5d lines, %5d sloc" % (
                        pathToFile, lang, linesSoFar, slocSoFar))
    except Exception as e:
        print("error reading '%s', skipping: %s" % (pathToFile, e))
    return linesSoFar, slocSoFar

def countLinesPython(pathToFile, options, lang):
    linesSoFar, slocSoFar = (0,0)
    if not pathToFile.endswith('.pb2.py'):
        linesSoFar, slocSoFar = _countLinesPython(pathToFile, options, lang)
    return linesSoFar, slocSoFar

def _countLinesPython(pathToFile, options, lang):
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
                print ("%-49s: %-4s %5d lines, %5d sloc" % (
                    pathToFile, lang, linesSoFar, slocSoFar))
    except Exception as e:
        print("error reading '%s', skipping: %s" % (pathToFile, e))
    return (linesSoFar, slocSoFar)


def countLinesRuby(pathToFile, options, lang):
    linesSoFar,slocSoFar    = (0,0)
    if not pathToFile.endswith('.pb.rb'):
        linesSoFar, slocSoFar = countLinesGeneric(pathToFile, options, lang)
    return linesSoFar, slocSoFar

def countLinesSnobol(pathToFile, options, lang):
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
                print ("%-49s: %-4s %5d lines, %5d sloc" % (
                        pathToFile, lang, linesSoFar, slocSoFar))
    except Exception as e:
        print("error reading '%s', skipping: %s" % (pathToFile, e))
    return linesSoFar, slocSoFar

