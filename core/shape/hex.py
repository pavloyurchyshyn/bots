from typing import List
from math import cos, sin, sqrt, dist, radians
from core.shape.base import CollideInterface
from core.shape.constants import ShapeType, Vector2DType


# https://www.redblobgames.com/grids/hexagons/#basics
class Hex(CollideInterface):
    SHAPE_TYPE = ShapeType.Hexagon

    def __init__(self, x: int, y: int, r: int, angle=0, collide_able=True):
        """
        r = outer circle
        """
        self.r = r
        self.position = x, y
        self.angle = angle
        self.collide_able = collide_able
        self._dots: List[Vector2DType] = []
        self.width = self.get_tile_width(r)
        self.height = self.get_tile_height(r)

        self.inner_circle_r = self.get_tile_inner_circle_r(r)
        self.h_distance = self.get_h_tile_distance(r)
        self.center = self.get_tile_center(x, y, r)
        self.build_dots()

    def rebuild(self, r=None):
        r = self.r if r is None else r
        self.r = r
        self.height = self.get_tile_height(r)
        self.inner_circle_r = self.get_tile_inner_circle_r(r)
        self.h_distance = self.get_h_tile_distance(r)
        self.center = self.get_tile_center(*self.position, r)
        self.build_dots(r)

    @property
    def radius(self):
        return self.inner_circle_r

    @property
    def rect(self):
        return *self.position, self.width, self.height

    @property
    def size(self):
        return self.width, self.height

    @staticmethod
    def get_tile_center(x, y, outer_r):
        return x + outer_r, y + Hex.get_tile_inner_circle_r(outer_r)

    @staticmethod
    def get_h_tile_distance(outer_r):
        return Hex.get_tile_width(outer_r) * 0.75

    @staticmethod
    def get_tile_inner_circle_r(outer_r):
        return Hex.get_tile_height(outer_r) / 2

    @staticmethod
    def get_tile_width(outer_r):
        return outer_r + outer_r

    @staticmethod
    def get_tile_height(outer_r):
        return sqrt(3) * outer_r

    def build_dots(self, r=None):
        r = self.r if r is None else r

        self.dots.clear()
        self.dots.append(self.center)

        x0, y0 = self.center

        for i in range(6):
            angle_rad = radians(60 * i)
            self._dots.append((int(x0 + r * cos(angle_rad)),
                               int(y0 + r * sin(angle_rad))))

    @property
    def dots(self):
        if self.collide_able:
            return self._dots

        return ()

    def move_to(self, xy: Vector2DType, r=None, *args, **kwargs) -> None:
        self.position = xy
        self.rebuild(r)

    def collide_circle(self, xy: Vector2DType, r) -> bool:
        return dist(xy, self.center) <= self.inner_circle_r + r

    def collide_point(self, xy: Vector2DType) -> bool:
        return dist(xy, self.center) <= self.inner_circle_r

    def collide(self, other) -> bool:
        """
        Returns True if collide object

        :param other:
        :return: bool
        """

        if self.collide_able:
            if other.SHAPE_TYPE == self.SHAPE_TYPE:
                return self.collide_hex(other)

            elif other.SHAPE_TYPE == ShapeType.Rect:
                return other.collide_circle(self.center, self.inner_circle_r)

            elif other.SHAPE_TYPE == ShapeType.Line:
                return other.collide_circle(self.center, self.inner_circle_r)

            elif other.SHAPE_TYPE == ShapeType.Point:
                return self.collide_point(other.center)

            elif other.SHAPE_TYPE == ShapeType.Circle:
                return self.collide_circle(other.center, other.radius)

            return self.collide_dots(other)
        else:
            return 0

    def collide_hex(self, other):
        return self.collide_circle(other.center, other.inner_circle_r)
        # return dist((self.center[0], 0), (other.center[0], 0)) <= (self.width + other.width)//2*0.75 and \
        #        dist((0, self.center[1]), (0, other.center[1])) <= (other.height + self.height)

        # return dist(self.center, other.center) <= self._distance and dist((0, self.center[1]),
        #                                                                     (0, other.center[1]) <= self._height / 2)

    def collide_any_obj_dot(self, obj) -> bool:
        for dot in obj.dots:
            if self.collide_point(dot):
                return True

        return False

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]