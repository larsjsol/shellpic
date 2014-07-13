#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Lars Jørgen Solberg <supersolberg@gmail.com> 2014
#

from distutils.core import setup
import pkg_resources

setup(
    name='Shellpic',
    version='1.5',
    author='Lars Jørgen Solberg',
    author_email='supersolberg@gmail.com',
    packages=['shellpic'],
    scripts=['bin/shellpic'],
    url='https://github.com/larsjsol/shellpic',
    license='GPLv3',
    description='Display images using escape codes',
    long_description=open('README.rst').read(),
    install_requires=[
        "Pillow",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Artistic Software",
        "Topic :: Games/Entertainment",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Graphics :: Viewers",
        "Topic :: Utilities",
        ],
)
