from core.shape.base import CollideInterface
from abc import ABC
from core.shape.constants import *


class Rectangle(CollideInterface, ABC):
    SHAPE_TYPE = ShapeType.Rect

    def __init__(self, x, y, size_x, size_y=None):
        self.size_x = size_x
        self.original_size_x = size_x
        self.original_size_y = size_y if size_y is not None else size_x
        self.size_y = size_y if size_y is not None else size_x

        self.center = x + self.size_x // 2, y + self.size_y // 2
        self._size = self.size_x if self.size_x < self.size_y else self.size_y
        self.x0 = x
        self.x1 = x + self.size_x
        self.y0 = y
        self.y1 = y + self.size_y

        self.h_size = self._size / 2
        self._dots = []
        self.build_dots()

        self._collide_able = 1

    def get_size(self):
        return self._size

    def build_dots(self):

        x0, y0 = self.x0, self.y0
        x1, y1 = self.x1, self.y1

        self._dots.clear()
        self._dots.append(self._center)
        self._dots.append((x0, y0))  # left top
        self._dots.append(((x0 + x1) // 2, y0))  # mid top
        self._dots.append((x1, y0))  # right top
        self._dots.append((x1, (y1 + y0) // 2))  # right mid
        self._dots.append((x1, y1))  # right bot
        self._dots.append(((x0 + x1) // 2, y1))  # mid bot
        self._dots.append((x0, y1))  # left bot
        self._dots.append((x0, (y1 + y0) // 2))  # left mid

    def change_position(self, xy):
        self._change_position(xy)

    def move(self, xy: tuple):
        self._change_position_lt(xy)

    def _change_position_lt(self, xy: tuple):
        """
        New left top corner

        :param xy: int, int
        :return:
        """
        x, y = xy
        self._center = [x + self.size_x // 2, y + self.size_y // 2]
        self.x0 = x
        self.y0 = y

        self.x1 = x + self.size_x
        self.y1 = y + self.size_y
        self.build_dots()

    def set_y(self, y):
        self._change_position_lt((self.x0, y))

    def _change_position(self, xy: tuple):
        """
        XY -> center of object

        :param xy: int, int
        :return:
        """
        x, y = xy
        self._center = xy
        self.x0 = x - self.size_x // 2
        self.y0 = y - self.size_y // 2

        self.x1 = x + self.size_x // 2
        self.y1 = y + self.size_y // 2
        self.build_dots()

    # dot inside the rectangle?
    def collide_point(self, xy: tuple) -> bool:
        return self.x0 <= xy[0] <= self.x1 and self.y0 <= xy[1] <= self.y1

    # did circle inside rectangle?
    def collide_circle(self, xy: tuple, r) -> bool:
        return self.x0 - r <= xy[0] <= self.x1 + r and self.y0 - r <= xy[1] <= self.y1 + r

    def collide_any_obj_dot(self, obj: CollideInterface) -> bool:
        return self.collide_dots(obj.dots)

    def collide(self, other) -> bool:
        if self._collide_able:
            other_type = other.SHAPE_TYPE
            if other_type == ShapeType.Rect:
                return self.collide_dots(other)

            elif other_type == ShapeType.Circle:
                return self.collide_circle(other.center, other.radius)

            elif other_type == ShapeType.Line:
                return other.collide_rect(self)

            elif other_type == ShapeType.Point:
                return self.collide_point(other.center)

        return 0

    @property
    def dots(self):
        if self._collide_able:
            return self._dots

        return ()

    @property
    def left_top(self):
        return self.x0, self.y0

    @property
    def left_bot(self):
        return self.x0, self.y1

    @property
    def right_bot(self):
        return self.x1, self.y1

    @property
    def right_top(self):
        return self.x1, self.y0

    @property
    def size(self):
        return self.size_x, self.size_y

    def get_rect(self):
        return self.x0, self.y0, self.size_x, self.size_y
