# SPDX-FileCopyrightText: Copyright (c) 2021 Jose David
#
# SPDX-License-Identifier: MIT
"""
`arrowline`
================================================================================

Utility function to draw arrow lines using vectorio and tilegride to display it


* Author(s): Jose David M

Implementation Notes
--------------------

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

import math
import displayio
from vectorio import Polygon, Circle

try:
    from typing import Optional
except ImportError:
    pass

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/CircuitPython_ArrowLine.git"


class Line:

    """A Line Arrow utility.

    :param grid: Tilegrid object where the bitmap will be located, set to None for
     arbitrary placement of the :class:`Line` (default = None)

    :param int x1: line first point x coordinate
    :param int y1: line first point x coordinate
    :param int x2: line first point x coordinate
    :param int y2: line first point x coordinate

    :param int arrow_length: arrow length in pixels. Arrow width is half of the length

    :param `displayio.Palette` palette: palette object used to display the bitmap.
     This is used to have the same color for the arrow
    :param int pal_index: pallet color index used in the bitmap to give the arrow line the color
     property

    :param int line_width: the width of the arrow's line, in pixels (default = 1)
    :param bool solid_line: indicates if the line is a solid line. Defaults to `True`
    :param int line_length: Length in pixels of the line.
     combinations of line_length and line_space. Defaults to 5.
    :param int line_space: Line space in pixels. Defaults to 5

    :param str pointer: point type. Two pointers could be selected :const:`C` Circle
     or :const:`A` Arrow. Defaults to Arrow

    :return: `displayio.Group`


    **Quickstart: Importing and using line_arrow**

    Here is one way of importing the :class:`Line` class so you can use:

    .. code-block:: python

        import displayio
        import board
        from CircuitPython_ArrowLine import Line
        display = board.DISPLAY
        my_group = displayio.Group()
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

        my_line = Line(screen_tilegrid, bitmap, 40, 90, 90, 60, 12, screen_palette, 1)

    Once you setup your display, you can now add ``my_line`` to your display using:

    .. code-block:: python

        my_group.append(line)
        display.show(my_group)


    **Summary: `arrowline` Features and input variables**

    The :class:`Line` widget has some options for controlling its position, visible appearance,
    and scale through a collection of input variables:

        - **position**: :const:`x1`, :const:`y1`, :const:`x2`, :const:`y2`

        - **size**: line length is given by two points. :const:`arrow_length`

        - **color**: :const:`pal_index`

        - **background color**: :const:`background_color`

    """

    def __init__(
        self,
        grid: Optional[displayio.TileGrid] = None,
        x1: int = 0,
        y1: int = 0,
        x2: int = 10,
        y2: int = 10,
        arrow_length: int = 10,
        palette: Optional[displayio.Palette] = None,
        pal_index: int = 1,
        line_width: int = 1,
        solid_line: bool = True,
        line_length: int = 5,
        line_space: int = 5,
        pointer: str = "A",
    ) -> None:
        if palette is None:
            raise ValueError("Must provide a valid palette")
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self._arrow_length = arrow_length
        self.line_width = line_width

        self.line_length = line_length
        self.line_space = line_space

        self.my_group = displayio.Group()

        self.arrow_palette = displayio.Palette(2)

        self.arrow_palette[1] = palette[pal_index]

        if grid is not None:
            self.x_reference = grid.x
            self.y_reference = grid.y
        else:
            self.x_reference = 0
            self.y_reference = 0

        self._angle = math.atan2((y2 - y1), (x2 - x1))

        angle2 = math.pi / 2 - self._angle
        arrow_side_x = arrow_length // 2 * math.cos(angle2)
        arrow_side_y = arrow_length // 2 * math.sin(angle2)

        self.x0 = int(math.ceil(arrow_length * math.cos(self._angle)))
        self.y0 = int(math.ceil(arrow_length * math.sin(self._angle)))

        start_x = self.x_reference + self.x2
        start_y = self.y_reference + self.y2

        self._arrow_base_x = start_x - self.x0
        self._arrow_base_y = start_y - self.y0

        self._distance = math.sqrt(
            ((self.x2 - self.x0) - x1) ** 2 + ((self.y2 - self.y0) - y1) ** 2
        )
        right_x = math.ceil(self._arrow_base_x + arrow_side_x)
        right_y = math.ceil(self._arrow_base_y - arrow_side_y)

        left_x = math.ceil(self._arrow_base_x - arrow_side_x)
        left_y = math.ceil(self._arrow_base_y + arrow_side_y)

        end_line_x = self.x2 - self.x0
        end_line_y = self.y2 - self.y0
        self.line_draw = _angledrectangle(
            self.x1, self.y1, end_line_x, end_line_y, stroke=self.line_width
        )

        if pointer == "A":
            arrow = Polygon(
                pixel_shader=self.arrow_palette,
                points=[(start_x, start_y), (right_x, right_y), (left_x, left_y)],
                x=0,
                y=0,
                color_index=1,
            )

            self.my_group.append(arrow)

        elif pointer == "C":
            circle_center_x = self.x_reference + self.line_draw[2][0]
            circle_center_y = self.y_reference + self.line_draw[2][1]

            circle_ending = Circle(
                pixel_shader=self.arrow_palette,
                radius=3,
                x=circle_center_x,
                y=circle_center_y,
                color_index=1,
            )

            self.my_group.append(circle_ending)

        if solid_line:
            self._solid_line()
        else:
            self._dotted_line()

    @property
    def draw(self) -> None:
        """
        Return the line object
        """
        return self.my_group

    def _solid_line(self) -> None:
        line_base = Polygon(
            pixel_shader=self.arrow_palette,
            points=[
                (
                    self.x_reference + self.line_draw[0][0],
                    self.y_reference + self.line_draw[0][1],
                ),
                (
                    self.x_reference + self.line_draw[1][0],
                    self.y_reference + self.line_draw[1][1],
                ),
                (
                    self.x_reference + self.line_draw[2][0],
                    self.y_reference + self.line_draw[2][1],
                ),
                (
                    self.x_reference + self.line_draw[3][0],
                    self.y_reference + self.line_draw[3][1],
                ),
            ],
            x=0,
            y=0,
            color_index=1,
        )
        self.my_group.append(line_base)

    def _dotted_line(self) -> None:
        distance = math.sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2)

        suma = self.line_length
        puntos = []
        puntos.append((self.x2, self.y2))
        while suma < distance:
            puntos.append(
                (
                    self.x2 - int(math.ceil(suma * math.cos(self._angle))),
                    self.y2 - int(math.ceil(suma * math.sin(self._angle))),
                )
            )
            suma = suma + self.line_length + self.line_space

        for i, ele in enumerate(puntos):
            if i == 0:
                continue
            if i % 2 == 0:
                _line = _angledrectangle(
                    ele[0],
                    ele[1],
                    puntos[i - 1][0],
                    puntos[i - 1][1],
                    stroke=self.line_width,
                )
                line_base = Polygon(
                    pixel_shader=self.arrow_palette,
                    points=[
                        (
                            self.x_reference + _line[0][0],
                            self.y_reference + _line[0][1],
                        ),
                        (
                            self.x_reference + _line[1][0],
                            self.y_reference + _line[1][1],
                        ),
                        (
                            self.x_reference + _line[2][0],
                            self.y_reference + _line[2][1],
                        ),
                        (
                            self.x_reference + _line[3][0],
                            self.y_reference + _line[3][1],
                        ),
                    ],
                    x=0,
                    y=0,
                    color_index=1,
                )

                self.my_group.append(line_base)


def _angledrectangle(x1, y1, x2, y2, stroke=1):
    # Code Source for this function by kmatch98 (R) 2021
    # https://github.com/adafruit/CircuitPython_Community_Bundle/pull/63
    if x2 - x1 == 0:
        xdiff1 = round(stroke / 2)
        xdiff2 = -round(stroke - xdiff1)
        ydiff1 = 0
        ydiff2 = 0

    elif y2 - y1 == 0:
        xdiff1 = 0
        xdiff2 = 0
        ydiff1 = round(stroke / 2)
        ydiff2 = -round(stroke - ydiff1)

    else:
        c_dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        xdiff = stroke * (y2 - y1) / c_dist
        xdiff1 = round(xdiff / 2)
        xdiff2 = -round(xdiff - xdiff1)

        ydiff = stroke * (x2 - x1) / c_dist
        ydiff1 = round(ydiff / 2)
        ydiff2 = -round(ydiff - ydiff1)

    return [
        (x1 + xdiff1, y1 + ydiff2),
        (x1 + xdiff2, y1 + ydiff1),
        (x2 + xdiff2, y2 + ydiff1),
        (x2 + xdiff1, y2 + ydiff2),
    ]
