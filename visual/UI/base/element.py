from abc import abstractmethod, ABC
from pygame import Surface

from global_obj import Global
from core.shape.constants import Vector2DType
from core.shape.rectangle import Rectangle, CollideInterface


class BaseUIAbs:
    uid: str
    tags: tuple = ()
    shape: CollideInterface or None
    position: Vector2DType
    surface: Surface
    parent_surface: Surface = Global.display

    @abstractmethod
    def render(self):
        raise NotImplementedError

    @abstractmethod
    def move(self, xy):
        raise NotImplementedError


class UpdateMixinAbs:
    @abstractmethod
    def update(self):
        raise NotImplementedError


class BaseUI(BaseUIAbs, ABC):
    def __init__(self, uid,
                 x_k=None, y_k=None,
                 shape_class: CollideInterface = Rectangle,
                 h_size_k=None, v_size_k=None,
                 auto_draw=False,
                 postpone_render=False,
                 parent: BaseUIAbs = None,
                 **kwargs):
        self.uid = uid

        self.auto_draw = auto_draw

        self.parent: BaseUIAbs = parent
        if parent:
            self.parent_surface = parent.surface

        self.x_k = x_k
        self.y_k = y_k
        self.x = 0
        self.y = 0

        self.size_x_k = h_size_k
        self.size_y_k = v_size_k
        self.h_size = 1
        self.v_size = 1

        self.surface = None
        self.shape_class = shape_class
        self.shape: CollideInterface or None = None

        if not postpone_render:
            self.build()

    def build(self):
        self.render()
        if self.auto_draw:
            self.draw()
        self.init_shape()

    def collide_point(self, point: Vector2DType) -> bool:
        if self.shape:
            return self.shape.collide_point(point)
        else:
            return False

    @abstractmethod
    def init_shape(self) -> None:
        raise NotImplementedError

    def draw(self):
        self.parent_surface.blit(self.surface, self.position)

    @abstractmethod
    def build_position(self) -> None:
        raise NotImplementedError

    @property
    def position(self):
        return self.x, self.y

    @position.setter
    def position(self, new_position):
        self.x, self.y = new_position
        self.render()

    @property
    def size(self) -> tuple[int, int]:
        return self.h_size, self.v_size
