from core.shape.base import CollideInterface
from core.shape.constants import ShapeType
from core.shape.constants import Vector2DType, DotsContainerType

from math import dist


class Point(CollideInterface):
    SHAPE_TYPE = ShapeType.Point

    def __init__(self, x: int, y: int, size: int = 1):
        self.size = size, size
        self.center = x, y

    @property
    def position(self):
        return self.center

    @property
    def x(self):
        return self.center[0]

    @property
    def y(self):
        return self.center[1]

    def move_to(self, xy: Vector2DType, *args, **kwargs) -> None:
        self.center = xy

    def build_dots(self):
        pass

    def collide_point(self, xy: list) -> bool:
        return self.center == xy

    def collide_dots(self, other) -> bool:
        for dot in other.dots:
            if self.collide_point(dot):
                return 1

        return 0

    def collide(self, other) -> bool:
        return other.collide_point(self.center)

    def collide_circle(self, xy: list, r) -> bool:
        return dist(xy, self.center) <= r

    @property
    def dots(self):
        return self.center,
