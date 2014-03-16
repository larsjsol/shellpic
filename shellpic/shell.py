#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Lars Jørgen Solberg <supersolberg@gmail.com> 2014
#

import shellpic

import os
import StringIO
import termios
import sys
import re

class Shell(shellpic.Formatter):
    def __init__(self):
        super(Shell, self).__init__()
        self._prev_frame = None

    @staticmethod
    def dimentions():
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
        termios.tcsetattr(sys.stdin, termios.TCSANOW, new_attrs)

        # ask for the cursor position
        print chr(27) +'[6n',
        # read the response from the terminal
        response = ''
        while True:
            char = sys.stdin.read(1)
            response += char
            if char == 'R':
                break

        # restore terminal attributes
        termios.tcsetattr(sys.stdin, termios.TCSANOW, old_attrs)

        # parse the response and return
        m = re.match(r'\033\[(\d+);(\d+)R', response)
        y, x = m.groups()
        return [int(x) - 1, int(y) - 1]

    def move_cursor(self,  pos_x, pos_y):
        return "{}[{};{}f".format(chr(27), self._origin[1] + pos_y,
                                  self._origin[0] + pos_x)

    @staticmethod
    def save_cursor():
        return "{}[s".format(chr(27))

    @staticmethod
    def restore_cursor():
        return "{}[r".format(chr(27))

    @staticmethod
    def clear_screen():
        return "[{}[2J".format(chr(27))

    @classmethod
    def colorcode(cls, bgcolor, fgcolor):
        raise NotImplementedError()

    def adjust_origin(self):
        self._origin = self.probe_cursor_pos()

    def need_repaint(self, pixels, x, y):
        if pixels[x][y] != self._prev_frame[x][y]:
            return True
        elif pixels[x][y + 1] != self._prev_frame[x][y + 1]:
            return True
        else:
            return False

    def color(self, pixels, dispose, x, y):
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

        file_str = StringIO.StringIO()

        width, height = image.size
        # since we put two pixels on top of each other in each character position
        # we must add a row for images with a odd numbered height
        padded_height = height if height % 2 == 0 else height + 1

        if not self._prev_frame:
            # create some empty space to draw on
            file_str.write('\n' * (padded_height / 2))

            # find out where we shold put the top left pixel if we are
            # in a terminal. Just use (0, 0) if we are piping to or
            # from files
            if os.isatty(sys.stdin.fileno()) and os.isatty(sys.stdout.fileno()):
                x, y = self.probe_cursor_pos()
                term_width, term_height = self.dimentions()
                if y + (padded_height / 2) > term_height:
                    adjust = (y + (padded_height / 2)) - term_height
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
                    file_str.write(self.move_cursor(x, y / 2))
                    file_str.write(self.colorcode(self.color(pixels, dispose_pixels, x, y),
                                                  self.color(pixels, dispose_pixels, x, y + 1)))
        file_str.write(self.move_cursor(width, padded_height / 2))
        file_str.write(chr(27) + u"[0m")
        return file_str.getvalue()

class Shell8bit(Shell):
    def __init__(self):
        super(Shell8bit, self).__init__()

    @classmethod
    def colorcode(cls, bgcolor, fgcolor):
        return u"{}[48;5;{};38;5;{}m{}▄ ".format(chr(27), cls.color_value_8bit(*bgcolor),
                                                 cls.color_value_8bit(*fgcolor), chr(8))

    @staticmethod
    def color_value_8bit(r, g, b, a=255):
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
