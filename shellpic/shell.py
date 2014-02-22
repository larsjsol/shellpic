#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Lars Jørgen Solberg <supersolberg@gmail.com> 2014
#

from shellpic.formatter import Formatter

import os
import StringIO


class Shell8bit(Formatter):
    def __init__(self):
        super(Shell8bit, self).__init__()

    def format(self, image):

        def off(x, y):
            """ the string offset for a coordinate """
            return (y * width) + x

        # convert the image to RGB color and extract each channel
        image = image.convert("RGB")

        pixels = image.getdata()
        width, height = image.size

        file_str = StringIO.StringIO()

        for y in range(0, height - 1, 2):
            for x in range(0, width):
                file_str.write(u"{}[48;5;{};38;5;{}m{}▄ ".format(chr(27),
                                                                 Shell8bit.color(*pixels[off(x, y)]),
                                                                 Shell8bit.color(*pixels[off(x, y + 1)]),
                                                                 chr(8)))
            file_str.write(chr(27) + u"[0m\n")
        if height % 2 == 0:
            y = height - 1
            for x in range(0, width):
                file_str.write(u"{}[48;5;{};38;5;{}m{}▄ ".format(chr(27),
                                                                 Shell8bit.color(*pixels[off(x, y)]),
                                                                 Shell8bit.color(0, 0, 0),
                                                                 chr(8)))
        file_str.write(chr(27) + u"[0m\n")
        return file_str.getvalue()


    @staticmethod
    def color(r, g, b):
        # basically the opposite of what is done in 256colres.pl from the xterm source
        r = (r - 55) / 40 if r > 55 else 0
        g = (g - 55) / 40 if g > 55 else 0
        b = (b - 55) / 40 if b > 55 else 0
        code = 16 + (r * 36) + (g * 6) + b

        return code

    @staticmethod
    def dimentions():
        rows, columns = os.popen('stty size', 'r').read().split()
        return (int(columns), int(rows))
