# pySloc/__init__.py

from abc import ABCMeta, abstractmethod, abstractproperty
import binascii, hashlib, os, re
from stat import *
from bs4 import BeautifulSoup, Comment

__all__ = [ '__version__',      '__version_date__',
            'countLinesInDir',
            'countLinesBash',   'countLinesC',      # 'countLinesGeneric',
            'countLinesGo',     
            'countLinesHtml',     
            'countLinesJava',   'countLinesOcaml',
            'countLinesNotSharp',
            'countLinesPython', 'countLinesRuby',   'countLinesShell',
            'countLinesSnobol', 'countLinesText',
            'uncommentHtml',    'uncommentJava',
            # classes
            'K', 'Q',
          ]

# exported constants ------------------------------------------------
__version__      = '0.4.25'
__version_date__ = '2015-12-17'

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
            'asm'       : countLinesNotSharp,       # s, S, asm
            'bash'      : countLinesShell,          # bash shell
            'c'         : countLinesC,              # ansic
            'cpp'       : countLinesC,              # C++
            'csh'       : countLinesNotSharp,       # csh, tcsh
            'css'       : countLinesJavaStyle,      # css, as in stylesheets
            'gen'       : countLinesNotSharp,       # treat # as comment
            'go'        : countLinesGo,             # golang
            'html'      : countLinesHtml,           # html
            'java'      : countLinesJava,           # plain old Java
            'js'        : countLinesJavaStyle,      # Javascript
            'ml'        : countLinesOcaml,          # ocaml, tentative abbrev
            'not#'      : countLinesNotSharp,
            'occ'       : countLinesOccam,          # concurrent programming
            'py'        : countLinesPython,         # yes, Python
            'R'         : countLinesNotSharp,       # R
            'rb'        : countLinesRuby,           # ruby
            'sed'       : countLinesNotSharp,       # stream editor
            'sh'        : countLinesShell,          # shell script
            'sno'       : countLinesSnobol,         # snobol4
            'tcl'       : countLinesNotSharp,       # tcl, tk, itk
            'txt'       : countLinesText,           # plain text
            'xml'       : countLinesXml,
        }
        # Guesses language short name (abbrev) from file extension.
        # See sloccount's break_filelist for hints.
        # Note {pl,pm,perl,pl} => perl
        self._ext2Lang  = {
            'asm'       : 'asm',
            'bash'      : 'bash',                   # yes, never used
            'c'         : 'c',                      # ansi c
            'C'         : 'cpp',                    # C++
            'cc'        : 'cpp',                    # C++
            'cp'        : 'cpp',                    # C++
            'cpp'       : 'cpp',                    # C++
            'CPP'       : 'cpp',                    # C++
            'c++'       : 'cpp',                    # C++
            'cxx'       : 'cpp',                    # C++
            'csh'       : 'csh',
            'css'       : 'css',
            'go'        : 'go',                     # same counter as C, Java ?
            'h'         : 'c',                      # PRESUMED ANSI C
            'hh'        : 'cpp',                    # C++; I've never seen this
            'hpp'       : 'cpp',                    # C++
            'html'      : 'html',                   # no counter
            'itk'       : 'tcl',
            'java'      : 'java',
            'js'        : 'js',                     # javascript, node.js
            'md'        : 'md',                     # no counter
            'ml'        : 'ml',                     # ocaml
            'mli'       : 'ml',                     # ocaml extension
            'not#'      : 'not#',
            'occ'       : 'occ',
            'py'        : 'py',
            'R'         : 'R',                      # R programming language 
            'r'         : 'R',                      # R programming language 
            'rb'        : 'rb',
            'S'         : 'asm',
            's'         : 'asm',
            'sed'       : 'sed',
            'sh'        : 'sh',
            'sno'       : 'sno',
            'tcsh'      : 'csh',
            'tcl'       : 'tcl',
            'tk'        : 'tcl',
            'txt'       : 'txt',
            'xml'       : 'xml',
        }
        # Maps lang short name (abbrev) to fuller language name.
        # By convention, short names are limited to 4 chars.
        self._langMap = {
            'asm'       : 'assembler',
            'bash'      : 'bash',
            'c'         : 'ansic',
            'cpp'       : 'C++',
            'csh'       : 'csh',
            'css'       : 'css',
            'gen'       : 'generic',
            'go'        : 'golang',
            'html'      : 'html',
            'java'      : 'java',
            'js'        : 'javascript',
            'md'        : 'markdown',
            'ml'        : 'ocaml',
            'not#'      : 'not#',
            'occ'       : 'Occam',
            'py'        : 'python',
            'R'         : 'R',
            'rb'        : 'ruby',
            'sed'       : 'sed',
            'sh'        : 'shell',
            'sno'       : 'snobol4',
            'tcl'       : 'tcl',
            'txt'       : 'text',
            'xml'       : 'XML',
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
            return countLinesNotSharp
        else:
            return None

    def getLongName(self, s):
        """ Given a short file name, return the longer language name """
        if s in self._langMap:
            return self._langMap[s]
        else:
            return None
    def getLangSet(self):
        "Return a set containing all recognized language abbreviations"""
        return frozenset(self._langMap.keys())

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

        if verbose > 1:
            if ext != None:
                print("  %s: find ext '%s', GUESS lang %s" % (fileName, ext, lang))
            else:
                print("  %s: NO ext, GUESS lang %s" % (fileName, lang))

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
    k               = options.k
    langsCounted   = options.langsCounted
    q               = options.q
    verbose         = options.verbose
    lines, sloc = (0,0)
    files = os.listdir(pathToDir)
    if files:
        q = options.q
        for name in sorted(files):
            # consider exclusions ...
            if options.exRE is not None and options.exRE.search(name) is not None:
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
                    if (lang != None) and (lang in langsCounted):
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

# BASH ==============================================================

def countLinesBash(path, options, lang):
    return countLinesShell(path, options, lang)

# C =================================================================

def countLinesC(path, options, lang):
    l, s = 0,0
    if (not path.endswith('.pb-c.c')) and (not path.endswith('.pb-c.h')):
        l, s = countLinesJavaStyle(path, options, lang)
    return l, s

# NOT_SHARP =========================================================

def countLinesNotSharp(pathToFile, options, lang):
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

# GO ================================================================

def countLinesGo(pathToFile, options, lang):
    linesSoFar,slocSoFar    = (0,0)
    if not pathToFile.endswith('.pb.go'):
        linesSoFar, slocSoFar = countLinesJavaStyle(pathToFile, options, lang)
    return linesSoFar, slocSoFar

# HTML ==============================================================

def _findHtmlCode(text):
    """
    We are in a comment.  Return a ref to the beginning of the text
    outside the comment block (which may be '') and the value of inComment.
    """
    posn = text.find('-->') 
    if posn == -1:
        return '', True

    if posn + 3 < len(text):
        return text[posn+3:], False
    else:
        return '', False

def _findHtmlComment(text):
    """
    We are NOT in a comment.  Return a ref to any code found, a ref to the
    rest of the text, and the value of inComment.
    """
    posn = text.find('<!--')       # one-line comment

    if posn == -1:
        return text, '', False

    if posn + 4 < len(text):
        return text[:posn], text[posn+4:], True
    else:
        return text[:posn], '', True


def uncommentHtml(text, inComment):
    """
    Given a line of text, return a ref to any code found and the value of
    inComment, which may have changed.
    """
    code = ''
    text = text.strip()
    while text:
        if inComment:
            text, inComment = _findHtmlCode(text)
        else:
            chunk, text, inComment = _findHtmlComment(text.strip())
            code += chunk   # XXX INEFFICIENT

    return code, inComment

# A better definition of a comment is that it begins with <!-- and ends
# with --> but does not contain -- or >

def countLinesHtml(pathToFile, options, lang):
    linesSoFar,slocSoFar    = (0,0)
    inComment               = False
    try:
        lines, hash = checkWhetherAlreadyCounted(pathToFile, options)
        if (hash != None) and (lines != None):
            for line in lines:
                linesSoFar += 1

                code, inComment = uncommentHtml(line, inComment)
                if code:
                    code = code.strip()
                    if code:
                        slocSoFar += 1

            options.already.add(hash)
            if options.verbose:
                print ("%-49s: %-4s %5d lines, %5d sloc" % (
                    pathToFile, lang, linesSoFar, slocSoFar))

    except Exception as e:
        print("error reading '%s', skipping: %s" % (pathToFile, e))
    return (linesSoFar, slocSoFar)

# JAVA ==============================================================

def countLinesJava(pathToFile, options, lang):
    linesSoFar,slocSoFar    = (0,0)
    if not pathToFile.endswith('Protos.java'):
        linesSoFar, slocSoFar = countLinesJavaStyle(pathToFile, options, lang)
    return linesSoFar, slocSoFar

def _findJavaCode(text):
    """
    We are in a comment.  Return a ref to the beginning of the text
    outside the comment block (which may be '') and the value of inComment.
    """
    posn = text.find('*/') 
    if posn == -1:
        return '', True

    if posn + 2 < len(text):
        return text[posn+2:], False
    else:
        return '', False

def _findJavaComment(text):
    """
    We are NOT in a comment.  Return a ref to any code found, a ref to the
    rest of the text, and the value of inComment.
    """
    multiLine   = False
    posnOld     = text.find('/*')       # multi-line comment
    posnNew     = text.find('//')       # one-line comment

    if posnOld == -1 and posnNew == -1:
        return text, '', False

    if posnNew == -1:
        posn      = posnOld
        inComment = True
        multiLine = True
    else:
        # posnNew is non-negative
        if posnOld == -1 or posnOld > posnNew:
            posn      = posnNew
            inComment = False
        else:
            posn      = posnOld
            inComment = True
            multiLine = True

    if multiLine and (posn + 2 < len(text)):
        return text[:posn], text[posn+2:], inComment
    else:
        return text[:posn], '', inComment


def uncommentJava(text, inComment):
    """
    Given a line of text, return a ref to any code found and the value of
    inComment, which may have changed.
    """
    code = ''
    text = text.strip()
    while text:
        if inComment:
            text, inComment = _findJavaCode(text)
        else:
            chunk, text, inComment = _findJavaComment(text.strip())
            code += chunk   # XXX INEFFICIENT

    return code, inComment

def countLinesJavaStyle(pathToFile, options, lang):
    linesSoFar,slocSoFar    = (0,0)
    inComment               = False
    try:
        lines, hash = checkWhetherAlreadyCounted(pathToFile, options)
        if (hash != None) and (lines != None):
            for line in lines:
                linesSoFar += 1

                code, inComment = uncommentJava(line, inComment)
                if code:
                    code = code.strip()
                    if code:
                        slocSoFar += 1

            options.already.add(hash)
            if options.verbose:
                print ("%-49s: %-4s %5d lines, %5d sloc" % (
                    pathToFile, lang, linesSoFar, slocSoFar))

    except Exception as e:
        print("error reading '%s', skipping: %s" % (pathToFile, e))
    return (linesSoFar, slocSoFar)

# OCAML =============================================================

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

# OCCAM =============================================================

def countLinesOccam(pathToFile, options, lang):
    """
    Count lines in a file where the double dash ('--') is the comment
    marker.  That is, we ignore blank lines, lines consisting solely of
    spaces, and those starting with zero or more spaces followed by
    a double dash.
    """

    linesSoFar, slocSoFar = (0,0)
    try:
        lines, hash = checkWhetherAlreadyCounted(pathToFile, options)
        if (hash != None) and (lines != None):
            for line in lines:
                linesSoFar += 1
                # This could be made more efficient.
                line = line.strip()
                if len(line) > 0 and not line.startswith('--'):
                    slocSoFar += 1
            options.already.add(hash)
            if options.verbose:
                print ("%-49s: %-4s %5d lines, %5d sloc" % (
                        pathToFile, lang, linesSoFar, slocSoFar))
    except Exception as e:
        print("error reading '%s', skipping: %s" % (pathToFile, e))
    return linesSoFar, slocSoFar

# PYTHON ============================================================

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

# RUBY ==============================================================

def countLinesRuby(pathToFile, options, lang):
    linesSoFar,slocSoFar    = (0,0)
    if not pathToFile.endswith('.pb.rb'):
        linesSoFar, slocSoFar = countLinesNotSharp(pathToFile, options, lang)
    return linesSoFar, slocSoFar

# SHELL =============================================================

def countLinesShell(path, options, lang):
    return countLinesNotSharp(path, options, lang)

# SNOBOL ============================================================

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

# TEXT ==============================================================

def countLinesText(pathToFile, options, lang):
    """
    Count the lines in a text file.  We ignore empty lines and lines 
    consisting solely of spaces.
    """

    linesSoFar, slocSoFar = (0,0)
    try:
        lines, hash = checkWhetherAlreadyCounted(pathToFile, options)
        if (hash != None) and (lines != None):
            for line in lines:
                linesSoFar += 1
                # This could be made more efficient.
                line = line.strip()
                if len(line) > 0 :
                    slocSoFar += 1
            options.already.add(hash)
            if options.verbose:
                print ("%-49s: %-4s %5d lines, %5d sloc" % (
                        pathToFile, lang, linesSoFar, slocSoFar))
    except Exception as e:
        print("error reading '%s', skipping: %s" % (pathToFile, e))
    return linesSoFar, slocSoFar

# XML ===============================================================

def countLinesXml(pathToFile, options, lang):
    """
    Count the lines in an xml file.  We ignore empty lines and lines 
    consisting solely of spaces, and of course we ignore xml comments.
    """

    try:
        lines, hash = checkWhetherAlreadyCounted(pathToFile, options)
    except Exception as e:
        print("error reading '%s', skipping: %s" % (pathToFile, e))
        return 0,0

    try:
        lineCount, slocSoFar = (0,0)
        if (hash != None) and (lines != None):
            lineCount = len(lines)
            raw = '\n'.join(lines)
            soup = BeautifulSoup(raw)
            comments = soup.findAll(text=lambda text:isinstance(text,Comment))
            [comment.extract() for comment in comments]
           
            # soup begins with '<html><body><p>' and ends with 
            #</p></body></html> on a separate line.

            elm = soup.html.body.p
            stripped = str(elm)[3:-4]       # drop leading <p> and trailing </p>
            
            lines = stripped.split('\n')

            for line in lines:
                # This could be made more efficient.
                line = line.strip()
                if len(line) > 0 :
                    slocSoFar += 1
            options.already.add(hash)
            if options.verbose:
                print ("%-49s: %-4s %5d lines, %5d sloc" % (
                        pathToFile, lang, lineCount, slocSoFar))
    except Exception as e:
        print("error parsing '%s', skipping: %s" % (pathToFile, e))
    return lineCount, slocSoFar



