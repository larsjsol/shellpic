#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Lars Jørgen Solberg <supersolberg@gmail.com> 2014
#

from distutils.core import setup
import pkg_resources

# Pillow's first version 1.0 was released on 2010-07-31, it's after PIL 1.1.7
# (2009-11-15), so no need to restrain the version unless it's too new in the
# future.
imaging_requires = 'Pillow'
try:
    pkg_resources.get_distribution("Pillow")
except pkg_resources.DistributionNotFound:
    imaging_requires = 'PIL >= 1.1.7'

setup(
    name='Shellpic',
    version='1.1',
    author=u'Lars Jørgen Solberg',
    author_email='supersolberg@gmail.com',
    packages=['shellpic'],
    scripts=['bin/shellpic'],
    url='https://github.com/larsjsol/shellpic',
    license='GPLv3',
    description='Displays images using shellcodes',
    long_description=open('README.rst').read(),
    install_requires=[
        imaging_requires,
    ],
)
