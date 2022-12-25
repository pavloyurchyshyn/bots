from math import sin, cos, radians, dist
from core.shape.base import CircleAbs, CollideInterface
from core.shape.constants import ShapeType, Vector2DType


class Circle(CircleAbs):
    """
    Circle object.
    """
    SHAPE_TYPE = ShapeType.Circle

    def __init__(self, x: int, y: int, r: int, angle=0, collide_able=True) -> None:
        self.angle = angle
        self.radius = r
        self.diameter: int = 2 * r  # radius
        self.size = self.diameter, self.diameter
        self.center: Vector2DType = [x, y]
        self.collide_able = collide_able
        self._dots = []
        self.build_dots()

    def move_to(self, xy: Vector2DType, *args, **kwargs) -> None:
        """
        Changing position of object center.
        :param xy: tuple(int, int)
        :return:
        """
        if self.center != xy:
            self.center = xy
            self.build_dots()

    def collide_circle(self, xy: Vector2DType, r) -> bool:
        """
        Returns True if circle on xy position with radius R collide object.

        :param xy: position of other object
        :param r: radius of other object
        :return:
        """

        return dist(xy, self.center) <= self.radius + r

    def collide_any_obj_dot(self, obj: CollideInterface) -> bool:
        return self.collide_dots(obj.dots)

    def collide_point(self, xy: Vector2DType) -> bool:
        """
        Returns True if dot inside circle, if range between center and dot <= radius

        :param xy: position of dot
        :return:
        """

        return dist(xy, self.center) <= self.radius

    def collide(self, other: CollideInterface) -> bool:
        """
        Returns True if collide object

        :param other:
        :return: bool
        """

        if self.collide_able:
            if other.SHAPE_TYPE == ShapeType.Circle:
                # other: Circle
                return self.collide_circle(other.center, other.radius)

            elif other.SHAPE_TYPE == ShapeType.Rect:
                return other.collide_circle(self.center, self.radius)

            elif other.SHAPE_TYPE == ShapeType.Line:
                return other.collide_circle(self.center, self.radius)

            elif other.SHAPE_TYPE == ShapeType.Point:
                return self.collide_point(other.center)

            elif other.SHAPE_TYPE == ShapeType.Hexagon:
                return self.collide_circle(other.circle, other.radius)

            else:
                return self.collide_any_obj_dot(other)

        else:
            return 0

    def build_dots(self):
        self._dots.clear()
        x, y = self.center
        self._dots.append(self.center)

        radius = self.radius

        for angle in range(0, 360, 30):
            x1: int = int(x + cos(radians(angle)) * radius)
            y1: int = int(y + sin(radians(angle)) * radius)
            self._dots.append((x1, y1))

    @property
    def dots(self):
        if self.collide_able:
            return self._dots

        return ()
