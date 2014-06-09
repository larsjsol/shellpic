#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Lars Jørgen Solberg <supersolberg@gmail.com> 2014
#

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import shellpic

import os
import io
import termios
import sys
import re
import functools


def memoize(obj):
# from https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer


class Shell(shellpic.Formatter):
    """
    A formatter for terminals, uses shell escape codes to draw images.

    This is an abstract class.
    """
    def __init__(self):
        super(Shell, self).__init__()
        self._prev_frame = None

    @staticmethod
    def dimentions():
        """
        Return the number of columns and rows in the current terminal.
        """
        rows, columns = os.popen('stty size < /dev/tty', 'r').read().split()
        return (int(columns), int(rows))

    @staticmethod
    def probe_cursor_pos():
        """
        Return the cursor position (x, y). This is an invasive
        procedure that involves changing the terminal attributes and
        printing to STDOUT and STDIN.

        STDIN and STDOUT must be connected to a terminal of some sort
        or else this method will fail.
        """

        assert os.isatty(sys.stdin.fileno())
        assert os.isatty(sys.stdout.fileno())

        # keep the current attrs so we can put them back when we are done
        old_attrs = termios.tcgetattr(sys.stdin)
        new_attrs = old_attrs[:]

        # disable echo and make sure input is sent char-by-char
        new_attrs[3] &= ~termios.ECHO
        new_attrs[3] &= ~termios.ICANON

        try:
            termios.tcsetattr(sys.stdin, termios.TCSANOW, new_attrs)
            termios.tcsetattr(sys.stdout, termios.TCSANOW, new_attrs)

            # ask for the cursor position
            sys.stdout.write(chr(27) + u'[6n')
            if sys.version_info[0] == 3:
                sys.stdout.flush()
            # read the response from the terminal
            response = u''

            while True:
                char = sys.stdin.read(1)
                response += char
                if char == u'R':
                    break

            # parse the response and return
            m = re.match(r'\033\[(\d+);(\d+)R', response)
            y, x = m.groups()

        finally:
            # restore terminal attributes
            termios.tcsetattr(sys.stdin, termios.TCSANOW, old_attrs)
            termios.tcsetattr(sys.stdout, termios.TCSANOW, old_attrs)

        return [int(x) - 1, int(y) - 1]

    def move_cursor(self,  pos_x, pos_y):
        return u"{0}[{1};{2}f".format(chr(27), self._origin[1] + pos_y,
                                  self._origin[0] + pos_x)

    @staticmethod
    def save_cursor():
        return u"{0}[s".format(chr(27))

    @staticmethod
    def restore_cursor():
        return u"{0}[r".format(chr(27))

    @staticmethod
    def clear_screen():
        return u"[{0}[2J".format(chr(27))

    @classmethod
    def colorcode(cls, bgcolor, fgcolor):
        """
        Return a string for drawing two pixels where one is placed
        above the other. The top pixel will be the color bgcolor and
        the bottom one will be fgcolor.

        This method must be implemented by a subclass.
        """
        raise NotImplementedError()

    def adjust_origin(self):
        """
        Examine the terminal to find where it should place the top
        left pixel of an image in order to fit in with the normal text
        flow.

        This is an invasive procedure that involves changing the
        terminal attributes and printing to STDOUT and STDIN.

        STDIN and STDOUT must be connected to a terminal of some sort
        or else this method will fail.
        """
        self._origin = self.probe_cursor_pos()

    def need_repaint(self, pixels, x, y):
        """
        Return True if the pixels at (x, y) or (x, y + 1) needs to be
        redrawn.
        """
        if pixels[x][y] != self._prev_frame[x][y]:
            return True
        elif pixels[x][y + 1] != self._prev_frame[x][y + 1]:
            return True
        else:
            return False

    def color(self, pixels, dispose, x, y):
        """
        Return the color at (x, y) taking into account previous frames
        and dispose.
        """
        rgba = pixels[x][y]
        if rgba[3] == 0:
            if dispose:
                rgba = dispose[x][y]
            elif self._prev_frame:
                rgba = self._prev_frame[x][y]
            else:
                rgba = (0, 0, 0, 255)
        self._prev_frame[x][y] = rgba
        return rgba

    def format(self, image, dispose=None):
        assert image.mode == 'RGBA'
        if dispose:
            assert dispose.mode == 'RGBA'

        file_str = io.StringIO()

        width, height = image.size
        # since we put two pixels on top of each other in each character position
        # we must add a row for images with a odd numbered height
        padded_height = height if height % 2 == 0 else height + 1

        if not self._prev_frame:
            # create some empty space to draw on
            file_str.write(u'\n' * (padded_height // 2))

            # find out where we shold put the top left pixel if we are
            # in a terminal. Just use (0, 0) if we are piping to or
            # from files
            if os.isatty(sys.stdin.fileno()) and os.isatty(sys.stdout.fileno()):
                x, y = self.probe_cursor_pos()
                term_width, term_height = self.dimentions()
                if y + (padded_height // 2) > term_height:
                    adjust = (y + (padded_height // 2)) - term_height
                    self._origin = x, y - adjust
                else:
                    self._origin = x, y

            # assume a black background
            self._prev_frame = [[[0, 0, 0, 255] for y in range(padded_height)] for x in range(width)]



        # put the pixels in a two-dimentional array
        pixels = shellpic.pixels(image)
        if padded_height != height:
            for x in range(width):
                pixels.append([0, 0, 0, 255])


        # put the dispose in a two-dimentional array
        if dispose:
            try:
                dispose_pixels = shellpic.pixels(dispose)
            except AttributeError:
                # i suppose things like are bound to happen when i depend on a undocumented property...
                dispose_pixels = [[[0, 0, 0, 255] for y in range(height)] for x in range(width)]

            if padded_height != height:
                for x in range(width):
                    dispose_pixels.append([0, 0, 0, 255])
        else:
            dispose_pixels = None

        # draw the image
        for y in range(0, height - 1, 2):
            for x in range(0, width):
                if self.need_repaint(pixels, x, y):
                    file_str.write(self.move_cursor(x, y // 2))
                    file_str.write(self.colorcode(self.color(pixels, dispose_pixels, x, y),
                                                  self.color(pixels, dispose_pixels, x, y + 1)))
        file_str.write(self.move_cursor(width, padded_height // 2))
        file_str.write(chr(27) + u"[0m")
        return file_str.getvalue()

class Shell8Bit(Shell):
    """
    A formatter designed for terminals capable of showing 256-colors
    (e.g. xterm and gnome-terminal).

    """
    def __init__(self):
        super(Shell8Bit, self).__init__()

    @staticmethod
    @memoize
    def colorcode(bgcolor, fgcolor):
        return u"{0}[48;5;{1};38;5;{2}m{3}▄ ".format(chr(27), Shell8Bit.color_value_8bit(*bgcolor),
                                                     Shell8Bit.color_value_8bit(*fgcolor), chr(8))

    @staticmethod
    def color_value_8bit(r, g, b, a=255):
        """
        Return the terminal color value corresponding to the r, g, b,
        parameters.

        The returned value can be passed to colorcode().
        """
        # basically the opposite of what is done in 256colres.pl from the xterm source
        r = (r - 55) // 40 if r > 55 else 0
        g = (g - 55) // 40 if g > 55 else 0
        b = (b - 55) // 40 if b > 55 else 0
        code = 16 + (r * 36) + (g * 6) + b

        return code

class Shell24Bit(Shell):
    """
    A formatter for terminals capable of displaying colors with a
    depth of 24 bits (e.g. terminal).
    """
    def __init__(self):
        super(Shell24Bit, self).__init__()

    @staticmethod
    @memoize
    def colorcode(bgcolor, fgcolor):
        return u"{0}[48;2;{1};{2};{3};38;2;{4};{5};{6}m{7}▄ ".format(chr(27), bgcolor[0], bgcolor[1], bgcolor[2],
                                                                     fgcolor[0], fgcolor[1], fgcolor[2], chr(8))

class Shell4Bit(Shell):
    """
    A formatter for 16-color terminals.
    """

    palette = (
        (0, 0, 0),       #  0 black
        (205, 0, 0),     #  1 red3
        (0, 205, 0),     #  2 green3
        (205, 205, 0),   #  3 yellow3
        (0, 0, 205),     #  4 blue3
        (205, 0, 205),   #  5 magenta3
        (0, 205, 205),   #  6 cyan
        (229, 229, 229), #  7 gray90
        (77, 77, 77),    #  8 gray30
        (255, 0, 0),     #  9 red
        (0, 255, 0),     # 10 green
        (255, 255, 0),   # 11 yellow
        (0, 0, 255),     # 12 blue
        (255, 0, 255),   # 13 magenta
        (0, 255, 255),   # 14 cyan
        (255, 255, 255), # 15 white
        )

    weights = (
        0.05,       #  0 black
        0.25,     #  1 red3
        1.2,     #  2 green3
        0.5,   #  3 yellow3
        1,     #  4 blue3
        0.5,   #  5 magenta3
        1,   #  6 cyan
        0.12, #  7 gray90
        0.12,    #  8 gray30
        0.5,     #  9 red
        1,     # 10 green
        0.75,   # 11 yellow
        1.25,     # 12 blue
        0.75,   # 13 magenta
        1.5,   # 14 cyan
        0.5, # 15 white
        )

    def __init__(self):
        super(Shell4Bit, self).__init__()

    @classmethod
    def color_value_4bit(cls, r, g, b, a=255):
        def distance(a, b):
            return sum([pow(x - y, 2) for x, y in zip(a, b)])
        distances = [[distance(p, [r, g, b]), i] for i, p in enumerate(cls.palette)]
        for d in distances:
            d[0] /= cls.weights[d[1]]
        distances.sort(key=lambda x: x[0])
        code = distances[0][1]
        code = 30 + code if code < 8 else 82 + code
        return code

    @staticmethod
    @memoize
    def colorcode(bgcolor, fgcolor):
        return u"{0}[{1};{2}m▄ ".format(chr(27), Shell4Bit.color_value_4bit(*bgcolor) + 10, 
                                        Shell4Bit.color_value_4bit(*fgcolor))
