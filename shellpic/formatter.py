#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Lars Jørgen Solberg <supersolberg@gmail.com> 2014
#

class Formatter(object):
    def __init__(self):
        super(Formatter, self).__init__()

    def format(self, image, dispose=None):
        raise NotImplementedError()

    @staticmethod
    def dimentions():
        raise NotImplementedError()

    @staticmethod
    def move_cursor(pos_x, pos_y):
        raise NotImplementedError()

    @staticmethod
    def save_cursor():
        raise NotImplementedError()

    @staticmethod
    def restore_cursor():
        raise NotImplementedError()

    @staticmethod
    def clear_screen():
        raise NotImplementedError()
