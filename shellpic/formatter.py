#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Lars Jørgen Solberg <supersolberg@gmail.com> 2014
#

class Formatter(object):
    def __init__(self):
        super(Formatter, self).__init__()

    def format(self, image):
        raise NotImplementedError()

    @staticmethod
    def dimentions():
        raise NotImplementedError()
