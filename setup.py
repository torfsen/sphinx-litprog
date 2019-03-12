#!/usr/bin/env python3
# encoding: utf-8

import os.path
import re

from setuptools import find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))

# Extract version
SOURCE_FILE = os.path.join(HERE, 'sphinx_litprog', '__init__.py')
version = None
with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        s = line.strip()
        m = re.match(r'''__version__\s*=\s*['"](.*)['"]''', line)
        if m:
            version = m.groups()[0]
if not version:
    raise RuntimeError('Could not extract version from "{}".'.format(SOURCE_FILE))


# Load long description from README.md
README = os.path.join(HERE, 'README.md')
with open(README, 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sphinx-litprog',
    description='A literate programming extension for Sphinx',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/torfsen/sphinx-litprog',
    version=version,
    license='MIT',
    keywords=['sphinx', 'literate programming'],
    classifiers=[
        # See https://pypi.org/classifiers/
        'Development Status :: 4 - Beta',
        'Framework :: Sphinx :: Extension',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Software Development :: Documentation',
    ],
    author='Florian Brucker',
    author_email='mail@florianbrucker.de',
    packages=find_packages(),
    install_requires=[
        'Sphinx>=1.8.0',
    ],
)

