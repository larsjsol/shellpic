#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Lars Jørgen Solberg <supersolberg@gmail.com> 2014
#

#pylint: disable=R0921
class Formatter(object):
    """
    A Formatter creates a string of unicode characters and escape
    codes that it shows a picture when viewed in the correct context,
    usually a terminal emulator.

    This is an abstract class.
    """

    def __init__(self):
        super(Formatter, self).__init__()
        self._origin = (0, 0) # cursor position where we put the upper left pixel

    def format(self, frame):
        """
        Convert image to a string and return it.
        """
        raise NotImplementedError()

    @staticmethod
    def dimensions():
        """
        Return a hint to the maximum image size suitable for this
        formatter.
        """
        raise NotImplementedError()

    def move_cursor(self, pos_x, pos_y):
        """
        Return a the command to move the cursor to a position as a string.
        """
        raise NotImplementedError()

    @staticmethod
    def save_cursor():
        """
        Return a string containing a command to save the cursor
        position.
        """
        raise NotImplementedError()

    @staticmethod
    def restore_cursor():
        """
        Return a string containing a command to restore the cursor
        position.
        """
        raise NotImplementedError()

    @staticmethod
    def clear_screen():
        """
        Return a string containing a command to clear the drawing
        area.
        """
        raise NotImplementedError()


    @classmethod
    def color_code(cls, r, g, b, a=255):
        """
        Convert the given color into the colorspace used by the
        formatter.
        """
        raise NotImplementedError()
