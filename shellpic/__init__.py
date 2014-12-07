#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Lars Jørgen Solberg <supersolberg@gmail.com> 2014
#

from __future__ import absolute_import
from __future__ import division


#pylint: disable=W0401
from shellpic.animation import *
from shellpic.formatter import *
from shellpic.shell import *
from shellpic.irc import *
from shellpic.nuts import *
from shellpic.tinymux import *

import PIL
from collections import Sequence

VERSION = "1.6.1"

def scale(image, width, height):
    """
    Scale image while preserving the aspect ratio
    """
    imgwidth, imgheight = image.size

    scalewidth = 1
    scaleheight = 1

    if imgwidth > width:
        scalewidth = width / (imgwidth + 2)
    if imgheight > height * 2:
        scaleheight = ((height - 1) * 2) / imgheight
    scale = min(scaleheight, scalewidth)
    return image.resize((int(imgwidth * scale), int(imgheight * scale)), PIL.Image.ANTIALIAS)

def ensure_rgb(palette, pixel):
    """
    Return the an rgb tuple for pixel, look it up in palette if
    necessary.
    """
    if isinstance(pixel, Sequence):
        return pixel[:3]
    else:
        return palette_lookup(palette, pixel)

def palette_lookup(palette, index):
    """
    Return the rgb value stored in the palette at the supplied index.
    """

    if sys.version_info[0] == 3:
        rgb = palette.palette[3 * index], palette.palette[(3 * index) + 1], palette.palette[(3 * index) + 2]
    else:
        rgb = ord(palette.palette[3 * index]), ord(palette.palette[(3 * index) + 1]), ord(palette.palette[(3 * index) + 2])
    return list(rgb)


def pixels(image):
    """
    Return the pixel values from an Image as a two-dimentional list.
    """
    width, height = image.size
    data = list(image.getdata())
    return [[data[(y * width) + x] for y in range(height)] for x in range(width)]
