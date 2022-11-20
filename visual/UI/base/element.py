from abc import abstractmethod, ABC
from pygame import Surface, SRCALPHA
from pygame.transform import smoothscale
from pygame.draw import rect as draw_rect, circle as draw_circle

from global_obj import Global

from core.shape.constants import Vector2DType
from core.shape import ShapeClasses, Rectangle

from visual.UI.constants.colors import CommonColors
from visual.UI.utils import get_surface
from visual.UI.constants.attrs import Attrs
from visual.UI.settings import UIDefault


class BaseUIAbs:
    colors = CommonColors
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
                 shape_class: ShapeClasses = Rectangle,
                 h_size_k=None, v_size_k=None,
                 auto_draw=False,
                 postpone_render=False,
                 parent: BaseUIAbs = None,
                 parent_surface=None,
                 **kwargs):
        self.uid: str = uid
        self.layer: int = kwargs.get(Attrs.Layer, 0)
        self.visible: bool = kwargs.get(Attrs.Visible, 1)
        self.active: bool = kwargs.get(Attrs.Active, 1)

        self.auto_draw = auto_draw

        self.parent: BaseUIAbs = parent
        if parent:
            self.parent_surface = parent_surface or parent.surface or Global.display
        else:
            self.parent_surface = parent_surface or Global.display

        self.x_k = x_k
        self.y_k = y_k
        self.x = 0
        self.y = 0

        self.size_x_k = h_size_k
        self.size_y_k = v_size_k if v_size_k else h_size_k
        self.h_size = int(self.parent_surface.get_width() * h_size_k) if h_size_k is not None else None
        self.v_size = int(self.parent_surface.get_height() * v_size_k) if v_size_k is not None else None

        self.surface_transparent = kwargs.get(Attrs.SurfaceTransparent, UIDefault.SurfaceTransparent)
        self.surface_flags = kwargs.get(Attrs.SurfaceFlags, UIDefault.SurfaceFlags)
        self.surface_color = kwargs.get(Attrs.SurfaceColor, UIDefault.SurfaceColor)

        self.from_left = kwargs.get(Attrs.FromLeft, False)
        self.from_bot = kwargs.get(Attrs.FromBot, False)
        self.from_top = kwargs.get(Attrs.FromTop, False)
        self.place_inside = kwargs.get(Attrs.PlaceInside, True)

        self.shape_class: ShapeClasses = shape_class
        self.shape: ShapeClasses or None = None

        if not postpone_render:
            self.build()

    def check_for_place_inside(self):
        h_size, v_size = self.surface.get_size()
        if self.place_inside:
            scale = 0
            if h_size > (h := self.parent_surface.get_width()):
                h_size = h
                scale = 1
            if v_size > (v := self.parent_surface.get_height()):
                v_size = v
                scale = 1

            if scale:
                self.surface = smoothscale(self.surface, (h_size, v_size))

    def default_build_position(self) -> None:
        h_size, v_size = self.surface.get_size()
        ph_size, pv_size = self.parent_surface.get_size()

        if self.x_k is not None:
            self.x = int(ph_size * self.x_k)
        elif self.from_left:
            self.x = 1
        else:
            self.x = (ph_size - h_size) // 2

        if self.y_k is not None:
            self.y = int(pv_size * self.y_k)
        elif self.from_bot and not self.from_top:
            self.y = pv_size - v_size
        elif self.from_top and not self.from_bot:
            self.y = 1
        else:
            self.y = (pv_size - v_size) // 2

    def build(self) -> None:
        self.render()
        self.build_position()
        if self.auto_draw:
            self.draw()
        self.init_shape()

    def collide_point(self, point: Vector2DType) -> bool:
        if self.shape:
            return self.shape.collide_point(point)
        else:
            return False

    def draw(self):
        if self.visible:
            self.parent_surface.blit(self.surface, self.position)
            if self.shape and Global.test_draw:
                for d in self.shape.dots:
                    draw_circle(self.parent_surface, (0, 255, 0), d, 2)

    def switch_active(self):
        self.active = not self.active

    def deactivate(self) -> None:
        self.active = 0

    def activate(self) -> None:
        self.active = 1

    def make_visible(self) -> None:
        self.visible = 1

    def make_invisible(self) -> None:
        self.visible = 0

    @property
    def position(self) -> tuple:
        return self.x, self.y

    @position.setter
    def position(self, new_position) -> None:
        self.x, self.y = new_position
        self.render()

    @property
    def size(self) -> tuple[int, int]:
        return self.h_size, self.v_size

    @property
    def real_position(self) -> Vector2DType:
        x, y = self.parent.real_position if self.parent else (0, 0)
        return x + self.x, y + self.y

    @abstractmethod
    def init_shape(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def build_position(self) -> None:
        raise NotImplementedError


class GetSurfaceMixin:
    def get_rect_surface(self, h_size, v_size=None, transparent=None, color=None, flags=None):
        flags = flags if flags is not None else getattr(self, Attrs.SurfaceFlags, SRCALPHA)
        transparent = transparent if transparent is not None else getattr(self, Attrs.SurfaceTransparent, 0)
        color = color if color is not None else getattr(self, Attrs.SurfaceColor, None)
        return get_surface(h_size, v_size,
                           transparent=transparent,
                           flags=flags,
                           color=color,
                           )


class DrawBorderMixin:
    def draw_border(self: BaseUI, surface=None, color=None):
        surface = surface if surface else self.surface
        color = color if color else getattr(self, Attrs.BorderColor, CommonColors.white)
        draw_rect(surface,
                  color,
                  ((0, 0), surface.get_size()),
                  getattr(self, Attrs.BorderSize, UIDefault.BorderSize),
                  getattr(self, Attrs.BorderRadius, UIDefault.BorderRadius),
                  getattr(self, Attrs.BorderTopLeftRadius, UIDefault.BorderTopLeftRadius),
                  getattr(self, Attrs.BorderTopRightRadius, UIDefault.BorderTopRightRadius),
                  getattr(self, Attrs.BorderBottomLeftRadius, UIDefault.BorderBottomLeftRadius),
                  getattr(self, Attrs.BorderBottomRightRadius, UIDefault.BorderBottomRightRadius),
                  )
