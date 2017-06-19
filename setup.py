#!/usr/bin/python3
# pysloc/setup.py

""" Set up distutils for pysloc. """

import re
from distutils.core import setup
__version__ = re.search(r"__version__\s*=\s*'(.*)'",
                        open('src/pysloc/__init__.py').read()).group(1)

# see http://docs.python.org/distutils/setupscript.html

setup(name='pysloc',
      version=__version__,
      author='Jim Dixon',
      author_email='jddixon@gmail.com',
      py_modules=[],
      packages=['src/pysloc'],
      # following could be in scripts/ subdir
      scripts=['src/pySloc', ],          # front end module(s)
      description='counts source lines of code for various languages',
      url='https://jddixon.github.io/pysloc',
      classifiers=[
          'Development Status :: 1 - Planning',
          'Development Status :: 2 - Pre-Alpha',
          'Development Status :: 3 - Alpha',
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python 3',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],)
