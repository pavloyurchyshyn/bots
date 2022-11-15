from abc import abstractmethod, ABC
from core.shape.constants import Vector2DType, DotsContainerType


class CollideInterface:
    SHAPE_TYPE: str = None
    collide_able: bool
    side_x: int
    side_y: int
    center: Vector2DType
    size: Vector2DType
    position: Vector2DType
    dots: DotsContainerType

    @abstractmethod
    def build_dots(self):
        raise NotImplementedError

    @abstractmethod
    def move_to(self, xy: Vector2DType, *args, **kwargs) -> None:
        raise NotImplementedError

    # did circle inside object
    @abstractmethod
    def collide_circle(self, xy: Vector2DType, r) -> bool:
        raise NotImplementedError

    @abstractmethod
    def collide_point(self, xy: Vector2DType) -> bool:
        raise NotImplementedError

    @abstractmethod
    def collide(self, other) -> bool:
        raise NotImplementedError

    @abstractmethod
    def collide_any_obj_dot(self, obj) -> bool:
        raise NotImplementedError

    def __contains__(self, item):
        return all(map(self.collide_point, item.dots))

    @property
    def side_x(self):
        return self.size[0]

    @property
    def side_y(self):
        return self.size[1]

    def collide_dots(self, dots: DotsContainerType) -> bool:
        """
        If at least one dot of object inside returns True.
        """
        for dot in dots:
            if self.collide_point(dot):
                return True

        return False


class CircleAbs(CollideInterface, ABC):
    radius: int
    diameter: int
    angle: int

    @property
    def position(self) -> Vector2DType:
        return self.center

    @property
    def x(self):
        return self.center[0]

    @property
    def y(self):
        return self.center[1]
