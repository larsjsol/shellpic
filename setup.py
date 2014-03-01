#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Lars Jørgen Solberg <supersolberg@gmail.com> 2014
#

from distutils.core import setup

setup(
    name='Shellpic',
    version='1.0.1',
    author=u'Lars Jørgen Solberg',
    author_email='supersolberg@gmail.com',
    packages=['shellpic'],
    scripts=['bin/shellpic'],
    url='http://pypi.python.org/pypi/Shellpic/',
    license='LICENSE',
    description='Displays images using shellcodes',
    long_description=open('README.rst').read(),
    install_requires=[
        "PIP >= 1.1.7",
    ],
)
