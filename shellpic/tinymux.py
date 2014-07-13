#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Marcos Marado <mindboosternoori@gmail.com> 2014
# This formatter is actually based on the IRC formatter from:
# Lars Jørgen Solberg <supersolberg@gmail.com> 2014
#

from __future__ import division

from shellpic.formatter import Formatter

import io

class Tinymux(Formatter):
    """
    A formatter for TinyMUX servers.
    """

    def __init__(self):
        super(Tinymux, self).__init__()

    @staticmethod
    def dimensions():
        return (70, 70) # maxsize allowed for object descriptions

    def format(self, frame):
        file_str = io.StringIO()

        file_str.write(u"%Xn%r")
        for y in range(0, frame.height, 2):
            for x in range(frame.width):
                if x > 0 and frame[x][y] == frame[x - 1][y]:
                    file_str.write(u".")
                else:
                    file_str.write(str(frame[x][y]) + u".")
            file_str.write(u"%Xn%r")
        file_str.write(u"%Xn%r")

        return file_str.getvalue()

    @classmethod
    def color_value(cls, r, g, b, a=255):
        if r == 0 and g == 0 and b == 0:
            return "%Xn%x<0 0 0>"
        else:
            return "%X<"+str(r)+" "+str(g)+" "+str(b)+">"+"%x<"+str(r)+" "+str(g)+" "+str(b)+">"
