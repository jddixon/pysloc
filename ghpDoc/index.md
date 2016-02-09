<h1 class="libTop">pysloc</h1>

pySloc is a Python 3 utility for counting lines of source code in a file,
directory,
or project.  It provides a count by language of source lines of code found
and a total for all languages.

## SLOC

Counting lines of source code is a crude measure of the size of a program
or project.  For most languages there is a conventional way to distinguish
comments; in C, for example, anything /* enclosed like this */ is considered
a comment and such comments can span more than one line.  In counting lines
of source code,

* comments are first removed
* then spaces at the beginning of the line are stripped off
* if there is anything left, it is considered a *Source Line Of Code*
and included in the SLOC count.

SLOC counts are useful for guesstimating how much effort will be required
to understand, fix, or replace code.  SLOC counts can also be used to coarsely
gage progress on a project.

Users should bear in mind, of course, that often cleaning up code will
reduce the SLOC count but improve performance and otherwise improve code
quality.

## Languages Handled

Languages are primarily distinguished by the extension on the file name.
Thus for example `example.py` would be counted according to the rules for
Python files whereas `example.java` would be treated as a Java file and
Java-style comments would be ignored in counting lines of source code.

Languages currently covered include, by short name,

* **asm**,	assembly language
* **aug**,	Augeas configuration editor
* **c**,	the venerable C programming language; ANSI C
* **csh**,	csh, another shell; tcsh is a variant
* **css**,	css, used for writing style sheets
* **go**,	Google's Go programming language
* **gperf**,hash function generator
* **hs**,	Haskell
* **html**,	the Web's markup language
* **java**,	the Sun programming language
* **js**,	javascript, the Web's programming language
* **json**,	JSON serializer
* **lex**,	lex/flex scanner
* **ml**,	Ocaml, a functional language
* **not#**,	'not#', a pseudo-language; counts any line whose first non-space character is not the sharp sign ('#')
* **occ**,	Occam, the concurrent programming language
* **perl**,	Perl, the sysadmin's language
* **proto**,Google Protobuf
* **py**,	Python
* **R**,	R, the statistics programming language
* **rb**,	Ruby
* **re2c**,	tool for writing fast lexers
* **scala**,Scala
* **sed**,	the language for `sed` scripts used to edit files from the command line
* **sh**,	bash or the shell, `sh`
* **sno**,	Snobol, the string-oriented programming language
* **tcl**,	the Tool Command Language, a dynamic scripting language
* **txt**,	plain text; counts all non-blank lines
* **xml**,	XML
* **yacc**,	yacc parser generator
* **yaml**,	YAML serializer

## Command Line

	usage: count lines of source code [-h] [-C [LANGSCOUNTED]] [-j] [-L MAINLANG]
	
                                      [-M MATCHES] [-S] [-t] [-v] [-V]
	                                  [-X EXCLUSIONS] [-z]
	                                  [namedFiles [namedFiles ...]]
	
	positional arguments:
	  namedFiles            any number of namedFiles and/or directories to scan
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -C [LANGSCOUNTED], --langsCounted [LANGSCOUNTED]
	                        colon-separated list of langugages to be counted
	                        (abbrev)
	  -j, --justShow        list options and exit
	  -L MAINLANG, --mainLang MAINLANG
	                        main language expected (short name, optional)
	  -M MATCHES, --matches MATCHES
	                        count ONLY files with matching names
	  -S, --sumSLOC         total up SLOC counts
	  -t, --showTimestamp   output UTC timestamp to command line
	  -v, --verbose         make me more chatty
	  -V, --showVersion     show version information
	  -X EXCLUSIONS, --exclusions EXCLUSIONS
	                        do not count files/directories with matching names
	  -z, --onlyNamedFiles  only count files named on the command line

Files named in the command line are always counted, even if their language
is not

## Deduping

Files are only counted once.  Differently put, if two files have identical
content, only the first encountered will be counted.

## Project Status

A good beta: usable for practical purposes.

