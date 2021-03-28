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


__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/jposada202020/CircuitPython_ArrowLine.git"

try:
    from vectorio import VectorShape, Polygon
    import displayio
    import bitmaptools
except ImportError:
    pass


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


    **Quickstart: Importing and using line_arrow**

    Here is one way of importing the `line_arrow` function so you can use:

    .. code-block:: python

        import displayio
        import board
        from CircuitPython_ArrowLine import arrowline
        display = board.DISPLAY
        my_group = displayio.Group(max_size=3)
        bitmap = displayio.Bitmap(100, 100, 5)
        screen_palette = displayio.Palette(3)
        screen_palette[1] = 0x00AA00
        screen_tilegrid = displayio.TileGrid(
            bitmap,
            pixel_shader=screen_palette,
            x=50,
            y=50,
        )
        my_group.append(screen_tilegrid)

    Now you can create an arrowline starting at pixel position x=40, y=90 using:

    .. code-block:: python

        my_line = line_arrow(screen_tilegrid, bitmap, 40, 90, 90, 60, 12, screen_palette, 1)

    Once you setup your display, you can now add ``my_line`` to your display using:

    .. code-block:: python

        my_group.append(line)
        display.show(my_group)


    **Summary: arrowline Features and input variables**

    The `arrowline` widget has some options for controlling its position, visible appearance,
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
