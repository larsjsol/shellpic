#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Lars Jørgen Solberg <supersolberg@gmail.com> 2014
#

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import division

import shellpic

import mimetypes
from PIL import Image


class Animation(object):

    def __init__(self, filename, animated=True):
        super(Animation, self).__init__()
        self.frames = []

        self.mimetype = mimetypes.guess_type(filename)

        if animated:
            self._explode(filename)
        else:
            img = Image.open(filename)
            self.frames = [Frame(img)]


    def _explode(self, filename):
        assert(self.mimetype[0] == 'image/gif')
        img = Image.open(filename)

        try:
            while True:
                self.frames.append(Frame(img))
                img.seek(img.tell() + 1)
        except EOFError:
            pass

    def scale(self, width, height):
        for f in self.frames:
            f.scale(width, height)

    def convert_colors(self, converter):
        for f in self.frames:
            f.convert_colors(converter)


class Frame(object):

    def __init__(self, image):
        super(Frame, self).__init__()

        self._pixels = None

        self.width, self.height = image.size

        if 'duration' in image.info:
            self.delay = image.info['duration'] / 1000
        else:
            self.delay = 0.5

        self.image = image.copy()

    def __getitem__(self, key):
        if not self._pixels:
            self.load()

        return self._pixels[key]

    def scale(self, width, height):
        self.image = shellpic.scale(self.image, width, height)
        self.width, self.height = self.image.size
        self._pixels = None

    def load(self):
        width, height = self.image.size

        self.image = self.image.convert('RGBA')
        self._pixels = shellpic.pixels(self.image)

        self.width = width
        self.height = height

        for y in range(height):
            for x in range(width):
                # use black as background color
                if self._pixels[x][y][3] != 255:
                    self._pixels[x][y] = [0, 0, 0, 255]

        # make sure that we have an even nuber of rows
        if height % 2 != 0:
            for x in range(width):
                self._pixels[x].append([0, 0, 0, 255])
            self.height += 1

    def convert_colors(self, converter):
        if not self._pixels:
            self.load()

        for x in range(self.width):
            for y in range(self.height):
                self._pixels[x][y] = converter(*self._pixels[x][y])
