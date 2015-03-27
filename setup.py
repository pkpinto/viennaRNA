#!/usr/bin/env python
# coding: utf-8

from sys import platform
from distutils.core import setup, Extension

version = "__version__ = '0.0.0'"
with open('viennaRNA/__version__.py', 'r') as f:
    version = f.read()
exec version

if platform == 'darwin':
    module = Extension('viennaRNA.viennarna', ['viennaRNA/viennarna.c'],
                       include_dirs=['/usr/local/include'],
                       library_dirs=['/usr/local/lib'],
                       libraries=['RNA'])
elif platform == 'linux2':
    module = Extension('viennaRNA.viennarna', ['viennaRNA/viennarna.c'],
                       libraries=['RNA'])
else:
    raise OSError('OS not supported.')

setup(name='viennaRNA',
      version=__version__,
      description='Wrapper for the Vienna RNA folding library',
      author='Paulo Pinto',
      author_email='pmsppinto@me.com',
      url='https://github.com/pmsppinto/viennaRNA',
      ext_modules=[module],
      packages=['viennaRNA'],)
