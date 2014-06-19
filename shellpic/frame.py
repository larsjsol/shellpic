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

class Frame(object):

    def __init__(self, image):
        super(Frame, self).__init__()
        self.pixels = None

        if hasattr(image, "dispose"):
            self._dispose = image.dispose
        else:
            self._dispose = None

        self.image = image.copy()

    def __getitem__(self, key):
        return self.pixels[key]

    def scale(self, width, height):
        self.image = shellpic.scale(self.image, width, height)
        if self._dispose:
            self._dispose = shellpic.scale(self._dispose, width, height)


    def load(self):
        width, height = self.image.size

        if self._dispose:
            self._dispose = self._dispose.convert('RGBA')
            try:
                self._dispose = shellpic.pixels(self._dispose)
            except AttributeError:
                # i suppose things like are bound to happen when i depend on a undocumented property...
                self._dispose = [[[0, 0, 0, 255] for y in range(height)] for x in range(width)]

        self.image = self.image.convert('RGBA')
        self.pixels = shellpic.pixels(self.image)

        for x in range(width):
            for y in range(height):
                rgba = self.pixels[x][y]
                if rgba[3] == 0:
                    if self._dispose:
                        rgba = self._dispose[x][y]
                    else:
                        rgba = (0, 0, 0, 0)
                self.pixels[x][y] = rgba

        # make sure that we have an even nuber of rows
        if height % 2 != 0:
            for x in range(width):
                self.pixels[x].append((0, 0, 0, 255))


    def convert_colors(self, converter):
        if not self.pixels:
            self.load()

        width, height = self.image.size
        for x in range(width):
            for y in range(height):
                self.pixels[x][y] = converter(*self.pixels[x][y])

