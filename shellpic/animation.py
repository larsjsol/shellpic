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

import subprocess
import tempfile
import os
import shutil
import re
from PIL import Image


class Animation(object):

    def __init__(self, filename, animated=True):
        super(Animation, self).__init__()
        self.frames = []

        img = Image.open(filename)
        if 'duration' in img.info:
            self.delay = img.info['duration'] / 1000
        else:
            self.delay = 0.5


        if animated:
            self._explode(filename)
        else:
            self.frames = [Frame(img)]


    def _explode(self, filename):
        def framenum(filename):
            m = re.search(r'\d+', filename)
            return int(m.group(0))

        #use imagemagick to turn each frame into a single file
        tmpdir = tempfile.mkdtemp()
        subprocess.call(["convert", "-coalesce", filename, os.path.join(tmpdir, "out.png")])
        files = os.listdir(tmpdir)
        files.sort(key=framenum)
        for f in files:
            img = Image.open(os.path.join(tmpdir, f))
            self.frames.append(Frame(img))
        shutil.rmtree(tmpdir)

    def scale(self, width, height):
        for f in self.frames:
            f.scale(width, height)

    def convert_colors(self, converter):
        for f in self.frames:
            f.convert_colors(converter)


class Frame(object):

    def __init__(self, image):
        super(Frame, self).__init__()
        self.pixels = None
        self.image = image

        self.width, self.height = image.size

    def __getitem__(self, key):
        return self.pixels[key]

    def scale(self, width, height):
        self.image = shellpic.scale(self.image, width, height)

    def load(self):
        width, height = self.image.size

        self.image = self.image.convert('RGBA')
        self.pixels = shellpic.pixels(self.image)

        self.width = width
        self.height = height

        for y in range(height):
            for x in range(width):
                if self.pixels[x][y][3] != 255:
                    self.pixels[x][y] = [0, 0, 0, 255]

        # make sure that we have an even nuber of rows
        if height % 2 != 0:
            for x in range(width):
                self.pixels[x].append([0, 0, 0, 255])
            self.height += 1

    def convert_colors(self, converter):
        if not self.pixels:
            self.load()

        for x in range(self.width):
            for y in range(self.height):
                self.pixels[x][y] = converter(*self.pixels[x][y])
