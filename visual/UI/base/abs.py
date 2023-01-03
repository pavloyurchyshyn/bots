from abc import abstractmethod
from visual.UI.constants.colors import CommonColors
from core.shape import ShapeClasses, Rectangle
from core.shape.constants import Vector2DType
from pygame import Surface
from global_obj import Global
from pygame.draw import circle as draw_circle
from typing import Union, Tuple
from visual.UI.constants.attrs import Attrs


BoolType = Union[bool, int]
ColorType = Tuple[int, int, int]


class StyleBaseAbs:
    color: ColorType
    from_left: BoolType
    from_bot: BoolType
    from_top: BoolType

    text_back_color: ColorType
    antialiasing_text: BoolType

    surface_transparent: BoolType
    surface_color: ColorType
    surface_flags: int
    antialiasing: BoolType

    border_color: ColorType
    border_size: int
    border_radius: int
    border_top_left_radius: int
    border_top_right_radius: int
    border_bottom_left_radius: int
    border_bottom_right_radius: int


class ButtonStyleBaseAbs(StyleBaseAbs):
    inacborder_color: ColorType

    inac_surface_transparent: BoolType
    inac_surface_color: ColorType
    inac_surface_flags: int


class BaseUIAbs:
    Colors = CommonColors
    uid: str
    layer: int
    tags: tuple = ()
    shape: ShapeClasses
    position: Vector2DType
    real_position: Vector2DType
    visible: bool
    active: bool
    surface: Surface
    parent_surface: Surface = Global.display
    size: tuple
    style: StyleBaseAbs

    @abstractmethod
    def draw(self) -> 'BaseUIAbs':
        raise NotImplementedError

    @abstractmethod
    def get_x(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_y(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def build(self, **kwargs):
        """
        Steps to completely build  element.
        """
        raise NotImplementedError

    @abstractmethod
    def render(self, **kwargs):
        """
        Render exactly surface.
        """
        raise NotImplementedError

    @abstractmethod
    def move(self, xy):
        raise NotImplementedError

    @abstractmethod
    def get_surface(self, **kwargs) -> Surface:
        """
        Returns base surface
        """
        raise NotImplementedError

    @abstractmethod
    def fill_surface(self, surface=None, color=None) -> None:
        raise NotImplementedError


class ShapeAbs:
    def __init__(self, shape_class: ShapeClasses = Rectangle,
                 **kwargs):
        self.shape_class: ShapeClasses = shape_class
        self.shape: ShapeClasses or None = None
        self.collideable = kwargs.get(Attrs.CollideAble, True)

    def collide_point(self, point: Vector2DType) -> bool:
        if self.shape:
            return self.shape.collide_point(point)
        else:
            return False

    @abstractmethod
    def init_shape(self) -> None:
        raise NotImplementedError

    def shape_test_draw(self) -> None:
        if self.shape and Global.test_draw:
            for d in self.shape.dots:
                draw_circle(self.parent_surface, (0, 255, 0), d, 2)
