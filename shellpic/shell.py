#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Lars Jørgen Solberg <supersolberg@gmail.com> 2014
#

from shellpic.formatter import Formatter

import os
import StringIO

class Shell(Formatter):
    def __init__(self):
        super(Shell, self).__init__()

    @staticmethod
    def dimentions():
        rows, columns = os.popen('stty size < /dev/tty', 'r').read().split()
        return (int(columns), int(rows))

    @classmethod
    def colorcode(cls, bgcolor, fgcolor):
        raise NotImplementedError()

    def format(self, image):
        def off(x, y):
            """ the string offset for a coordinate """
            return (y * width) + x

        # convert the image to RGB color and extract each channel
        image = image.convert("RGB")

        pixels = image.getdata()
        width, height = image.size

        file_str = StringIO.StringIO()

        yrange = height if height % 2 == 0 else height - 1
        for y in range(0, yrange, 2):
            for x in range(0, width):
                file_str.write(self.colorcode(pixels[off(x, y)], pixels[off(x, y + 1)]))
            file_str.write(chr(27) + u"[0m\n")
        if height % 2 != 0:
            for x in range(0, width):
                file_str.write(self.colorcode(pixels[off(x, height - 1)], (0, 0, 0)))
            file_str.write(chr(27) + u"[0m\n")
        return file_str.getvalue()


class Shell8bit(Shell):
    def __init__(self):
        super(Shell8bit, self).__init__()

    @classmethod
    def colorcode(cls, bgcolor, fgcolor):
        return u"{}[48;5;{};38;5;{}m{}▄ ".format(chr(27), cls.color(*bgcolor),
                                                 cls.color(*fgcolor), chr(8))


    @staticmethod
    def color(r, g, b):
        # basically the opposite of what is done in 256colres.pl from the xterm source
        r = (r - 55) / 40 if r > 55 else 0
        g = (g - 55) / 40 if g > 55 else 0
        b = (b - 55) / 40 if b > 55 else 0
        code = 16 + (r * 36) + (g * 6) + b

        return code

class Shell24Bit(Shell):
    def __init__(self):
        super(Shell24Bit, self).__init__()

    @classmethod
    def colorcode(cls, bgcolor, fgcolor):
        return u"{}[48;2;{};{};{};38;2;{};{};{}m{}▄ ".format(chr(27), bgcolor[0], bgcolor[1], bgcolor[2],
                                                            fgcolor[0], fgcolor[1], fgcolor[2], chr(8))
