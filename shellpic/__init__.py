#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Lars Jørgen Solberg <supersolberg@gmail.com> 2014
#

from shell import *

def scale(image, width, height):
    """ scale an image while keeping the aspect ratio"""
    imgwidth, imgheight = image.size

    scalewidth = 1
    scaleheight = 1

    if imgwidth > width:
        scalewidth = float(width) / (imgwidth + 2)
    if imgheight > height * 2:
        scaleheight = float(height * 2) / imgheight

    return image.resize((int(imgwidth * scalewidth), int(imgheight * scaleheight)))
