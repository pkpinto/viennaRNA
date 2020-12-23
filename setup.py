#!/usr/bin/env python

import os
from sys import platform

from setuptools import setup, find_namespace_packages, Extension
from setuptools.command.build_ext import build_ext

API_REQUIRES = [
    # rest api
    'fastapi',
]
TEST_REQUIRES = [
    # testing and coverage
    'pytest<5.3', 'coverage', 'pytest-cov', 'pylint',
]

with open('README.md', 'r') as f:
    long_description = f.read()

# by default, the .so built includes the platform name,
# e.g. viennarna.cpython-37m-darwin.so, that is undesirable
# https://stackoverflow.com/a/60285245
class _build_ext(build_ext):
    def get_ext_filename(self, ext_name):
        filename = super().get_ext_filename(ext_name)
        return os.path.join(os.path.split(filename)[0], 'viennarna.so')

if platform == 'darwin':
    module = Extension('viennaRNA.viennarna', sources=['src/viennaRNA/viennarna.c'],
                       library_dirs=['../ViennaRNA-2.4.14/lib'],
                       include_dirs=['../ViennaRNA-2.4.14/include'],
                       libraries=['RNA'])
elif platform == 'linux':
    module = Extension('viennaRNA.viennarna', sources=['src/viennaRNA/viennarna.c'],
                       libraries=['RNA', 'mpfr', 'gmp'], extra_link_args=['-fopenmp', '-fno-lto'])
else:
    raise OSError('OS not supported.')

setup(
    name='viennaRNA',
    version='4.1-beta',
    description='Wrapper for the Vienna RNA folding library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
    ],
    url='https://github.com/pkpinto/viennaRNA',
    author='Paulo Kauscher Pinto',
    author_email='paulo.kauscher.pinto@icloud.com',
    license='Apache License 2.0',
    package_dir={'': 'src'},
    ext_modules=[module],
    cmdclass={'build_ext': _build_ext},
    packages=find_namespace_packages(where='src'),
    install_requires=[],
    extras_require={
        'api': API_REQUIRES,
        'test': TEST_REQUIRES,
    },
)
