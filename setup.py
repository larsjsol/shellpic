#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Lars Jørgen Solberg <supersolberg@gmail.com> 2014
#

from distutils.core import setup

setup(
    name='Shellpic',
    version='1.0.2',
    author=u'Lars Jørgen Solberg',
    author_email='supersolberg@gmail.com',
    packages=['shellpic'],
    scripts=['bin/shellpic'],
    url='https://github.com/larsjsol/shellpic',
    license='LICENSE',
    description='Displays images using shellcodes',
    long_description=open('README.rst').read(),
    install_requires=[
        "PIL >= 1.1.7",
    ],
)
