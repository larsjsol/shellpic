#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Marcos Marado <mindboosternoori@gmail.com> 2014
# This formatter is actually based on the IRC formatter from:
# Lars Jørgen Solberg <supersolberg@gmail.com> 2014
#

from __future__ import division

from shellpic.formatter import Formatter

import io

class Nuts(Formatter):
    """
    A formatter for NUTS talkers.
    """

    # mIRC palette according to http://forum.xchat.org/viewtopic.php?f=6&t=7719
    palette = (
        (0xff, 0xff, 0xff), #white
        (0x0, 0x0, 0x0),    #black
        (0x0, 0x0, 0x7f),   #blue (navy)
        (0x0, 0x93, 0x0),   #green
        (0xff, 0x0, 0x0),   #red
        (0x7f, 0x0, 0x0),   #brown (maroon)
        (0x9c, 0x0, 0x9c),  #purple
        (0xfc, 0x7f, 0x0),  #orange (olive)
        (0xff, 0xff, 0x0),  #yellow
        (0x0, 0xfc, 0x0),   #light green (lime)
        (0x0, 0x93, 0x93),  #teal
        (0x0, 0xff, 0xff),  #light cyan
        (0x0, 0x0, 0xfc),   #light blue
        (0xff, 0x0, 0xff),  #pink
        (0x7f, 0x7f, 0x7f), #grey
        (0xd2, 0xd2, 0xd2)  #light gray
        )

    # NUTS palette according to https://github.com/marado/Amnuts/blob/master/src/amnuts230.c#L8547
    npalette = (
        "~RS~OL~FW", # write
        "~RS~FK",    # black
        "~RS~FB",    # blue
        "~RS~FG",    # green
        "~RS~FR",    # red
        "~RS~FY",    # brown
        "~RS~FM",    # purple
        "~RS~OL~FR", # orange
        "~RS~OL~FY", # yellow
        "~RS~OL~FG", # light green
        "~RS~FC",    # teal
        "~RS~OL~FC", # light cyan
        "~RS~OL~FB", # light blue
        "~RS~OL~FM", # pink
        "~RS~OL~FK", # grey
        "~RS~FW",    # light gray
        )

    # colors with a higher weight will be used more often
    # i should probably figure out a better way to map colors...
    weights = (
    0.5, #white
    1,   #black
    1,   #blue (navy)
    2,   #green
    0.5, #red
    0.5, #brown (maroon)
    0.5, #purple
    0.5, #orange (olive)
    2,   #yellow
    2,   #light green (lime)
    2,   #teal
    0.5, #light cyan
    0.5, #light blue
    2,   #ping
    0.5, #grey
    0.5  #light gray
    )


    def __init__(self):
        super(Nuts, self).__init__()

    @staticmethod
    def dimensions():
        return (78, 78) # guesstimation of how much room is normally available in a chatwindow

    def format(self, frame):
        file_str = io.StringIO()

        for y in range(0, frame.height, 2):
            for x in range(0, frame.width):
                file_str.write(str(frame[x][y]) + u"█")
            file_str.write(u"\n")

        return file_str.getvalue()

    @classmethod
    def color_value(cls, r, g, b, a=255):
        # ugh, there is probably better way of doing this, but i can't make heads or tails of
        # the PIL documentation
        def distance(a, b):
            return sum([pow(x - y, 2) for x, y in zip(a, b)])
        distances = [[distance(p, [r, g, b]), i] for i, p in enumerate(cls.palette)]
        for d in distances:
            d[0] /= cls.weights[d[1]]
        distances.sort(key=lambda x: x[0])
        return cls.npalette[distances[0][1]]
