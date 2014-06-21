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
    def dimentions():
        return (70, 70) # maxsize allowed for object descriptions

    def format(self, image, dispose=None):
        def off(x, y):
            """ the string offset for a coordinate """
            return (y * width) + x

        assert image.mode == 'RGBA'

        width, height = image.size
        pixels = [self.color(*p) for p in image.getdata()]

        file_str = io.StringIO()

        yrange = height if height % 2 == 0 else height - 1
        file_str.write(u"%Xn%r")
        for y in range(0, yrange, 2):
            for x in range(0, width):
                if x>0 and pixels[off(x,y)] == pixels[off(x-1,y)]:
                    file_str.write(u".")
                else:
                    file_str.write(str(pixels[off(x, y)]) + u".")
            file_str.write(u"%Xn%r")
        if height % 2 != 0:
            for x in range(0, width):
                file_str.write(str(pixels[off(x, height - 1)]) + u".")
            file_str.write(u"%Xn%r")
        file_str.write(u"%Xn%r")
        return file_str.getvalue()

    @classmethod
    def color(cls, r, g, b, a):
        if r == 0 and g == 0 and b == 0:
            return "%Xn%x<0 0 0>";
        else:
            return "%X<"+str(r)+" "+str(g)+" "+str(b)+">"+"%x<"+str(r)+" "+str(g)+" "+str(b)+">";
