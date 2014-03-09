#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Lars Jørgen Solberg <supersolberg@gmail.com> 2014
#

from formatter import *
from shell import *
from irc import *

import PIL
from collections import Sequence

VERSION = "1.2"

def scale(image, width, height):
    """ scale an image while keeping the aspect ratio"""
    imgwidth, imgheight = image.size

    scalewidth = 1
    scaleheight = 1

    if imgwidth > width:
        scalewidth = float(width) / (imgwidth + 2)
    if imgheight > height * 2:
        scaleheight = float(height * 2) / imgheight
    scale = min(scaleheight, scalewidth)

    try:
        return image.resize((int(imgwidth * scale), int(imgheight * scale)), PIL.Image.ANTIALIAS)
    except ValueError:
        # the above sometimes fails with "ValueError: unknown filter"
        return image.resize((int(imgwidth * scale), int(imgheight * scale)))


def ensure_rgb(palette, pixel):
    if isinstance(pixel, Sequence):
        return pixel[:3]
    else:
        return palette_lookup(palette, pixel)

def palette_lookup(palette, index):
    return ord(palette.palette[3 * index]), ord(palette.palette[(3 * index) + 1]), ord(palette.palette[(3 * index) + 2])
