# SPDX-FileCopyrightText: 2021 Jose David M.
#
# SPDX-License-Identifier: MIT
#############################
"""
Example code for the graph showcased in the readme section
"""

import displayio
import board
from arrowline import Line


display = board.DISPLAY

my_group = displayio.Group()

bitmap = displayio.Bitmap(300, 300, 6)

screen_palette = displayio.Palette(5)
screen_palette[1] = 0x00AA00
screen_palette[2] = 0x0000FF
screen_palette[3] = 0x440044
screen_palette[4] = 0xFFFD37
screen_tilegrid = displayio.TileGrid(
    bitmap,
    pixel_shader=screen_palette,
    x=0,
    y=0,
)

my_group.append(screen_tilegrid)

a = Line(
    screen_tilegrid,
    50,
    280,
    250,
    50,
    12,
    screen_palette,
    1,
    line_width=3,
    solid_line=False,
    line_length=4,
    line_space=3,
)
my_group.append(a.draw)
b = Line(
    screen_tilegrid,
    180,
    100,
    240,
    280,
    12,
    screen_palette,
    2,
    solid_line=False,
    line_length=2,
    line_space=3,
)
my_group.append(b.draw)
c = Line(
    screen_tilegrid,
    100,
    99,
    150,
    100,
    12,
    screen_palette,
    2,
)
my_group.append(c.draw)
d = Line(
    screen_tilegrid,
    100,
    99,
    50,
    100,
    12,
    screen_palette,
    2,
)
my_group.append(d.draw)
e = Line(screen_tilegrid, 0, 0, 100, 50, 5, screen_palette, 3, pointer="C")
my_group.append(e.draw)
f = Line(screen_tilegrid, 320, 200, 320, 10, 20, screen_palette, 4, pointer="C")
my_group.append(f.draw)
display.show(my_group)
