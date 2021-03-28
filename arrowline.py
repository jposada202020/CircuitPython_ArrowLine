# SPDX-FileCopyrightText: Copyright (c) 2021 Jose David
#
# SPDX-License-Identifier: MIT
"""
`arrowline`
================================================================================

Utility function to draw arrow lines using vectorio and tilegride to display it


* Author(s): Jose David

Implementation Notes
--------------------

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# pylint: disable=too-many-lines, too-many-instance-attributes, too-many-arguments
# pylint: disable=too-many-locals, too-many-statements, invalid-name

import math
import displayio
from vectorio import VectorShape, Polygon
import bitmaptools

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/jposada202020/CircuitPython_ArrowLine.git"


def line_arrow(grid, bitmap_s, x1, y1, x2, y2, arrow_length, palette, pal_index):
    """A Line Arrow utility.

    :param grid: Tilegrid object where the bitmap will be located
    :param bitmap_s: bitmap object used to display the line and that is contain in the
     tilegrid

    :param int x1: line first point x coordinate
    :param int y1: line first point x coordinate
    :param int x2: line first point x coordinate
    :param int y2: line first point x coordinate

    :param int arrow_length: arrow length in pixels. Arrow width is half of the length

    :param palette: palette object used to display the bitmap. This is used to utilize the
     same color for the arrow
    :param pal_index: pallet color index used in the bitmap to give the arrow line the color
     property

    :return: vectorio VectorShape object to be added to the displayio group


     **Summary: arrowline Features and input variables**

    The `cartesian` widget has some options for controlling its position, visible appearance,
    and scale through a collection of input variables:

        - **position**: ``x1``, ``y1``, ``x2``, ``y2``

        - **size**: line length is given by two points. ``arrow_length``

        - **color**: ``pal_index``

        - **background color**: ``background_color``

    """

    bitmaptools.draw_line(bitmap_s, x1, y1, x2, y2, pal_index)

    angle = math.atan2((y2 - y1), (x2 - x1))
    x0 = arrow_length * math.cos(angle)
    y0 = arrow_length * math.sin(angle)

    angle2 = math.pi / 2 - angle
    arrow_side_x = arrow_length // 2 * math.cos(angle2)
    arrow_side_y = arrow_length // 2 * math.sin(angle2)

    start_x = grid.x + x2
    start_y = grid.y + y2

    arrow_base_x = start_x - x0
    arrow_base_y = start_y - y0

    right_x = math.ceil(arrow_base_x + arrow_side_x)
    right_y = math.ceil(arrow_base_y - arrow_side_y)

    left_x = math.ceil(arrow_base_x - arrow_side_x)
    left_y = math.ceil(arrow_base_y + arrow_side_y)

    arrow_palette = displayio.Palette(2)
    arrow_palette.make_transparent(0)
    arrow_palette[1] = palette[pal_index]

    arrow = Polygon(points=[(start_x, start_y), (right_x, right_y), (left_x, left_y)])
    arrow_vector_shape = VectorShape(
        shape=arrow,
        pixel_shader=arrow_palette,
        x=0,
        y=0,
    )
    return arrow_vector_shape
