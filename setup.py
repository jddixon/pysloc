#!/usr/bin/python3

# pysloc/setup.py

import re
from distutils.core import setup
__version__ = re.search("__version__\s*=\s*'(.*)'",
                        open('pysloc/__init__.py').read()).group(1)

# see http://docs.python.org/distutils/setupscript.html

setup(name='pysloc',
      version=__version__,
      author='Jim Dixon',
      author_email='jddixon@gmail.com',
      py_modules=[],
      packages=['pysloc'],
      # following could be in scripts/ subdir
      scripts=['pySloc', ],          # front end module(s)
      # MISSING url
      )
