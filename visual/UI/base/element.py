from abc import abstractmethod, ABC
from pygame import Surface, SRCALPHA
from pygame.draw import rect as draw_rect, circle as draw_circle

from global_obj import Global

from core.shape.constants import Vector2DType
from core.shape import ShapeClasses, Rectangle

from visual.UI.constants.colors import CommonColors
from visual.UI.utils import get_surface
from visual.UI.constants.attrs import Attrs
from visual.UI.settings import UIDefault


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

    @abstractmethod
    def draw(self):
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
        # color = getattr(self, Attrs.SurfaceColor, UIDefault.SurfaceColor) if color is None else color
        # surface = surface if surface else self.surface
        raise NotImplementedError
    # @abstractmethod
    # def build_position(self) -> None:
    #     raise NotImplementedError


class BaseUI(BaseUIAbs, ABC):
    def __init__(self, uid,
                 x_k=None, y_k=None,
                 h_size_k=1, v_size_k=1,
                 parent: BaseUIAbs = None,
                 parent_surface=None,
                 build_surface=True,
                 **kwargs):
        self.uid: str = uid
        self.layer: int = kwargs.get(Attrs.Layer, 0)
        self.visible: bool = kwargs.get(Attrs.Visible, 1)
        self.active: bool = kwargs.get(Attrs.Active, 1)

        self.parent: BaseUIAbs = parent

        if parent:
            self.parent_surface = parent_surface or parent.surface or Global.display
        else:
            self.parent_surface = parent_surface or Global.display

        self.from_left = kwargs.get(Attrs.FromLeft, False)
        self.from_bot = kwargs.get(Attrs.FromBot, False)
        self.from_top = kwargs.get(Attrs.FromTop, False)
        # self.keep_in_center = kwargs.get(Attrs.InCenter, False)
        # self.place_inside = kwargs.get(Attrs.PlaceInside, True)

        self.h_size_k = h_size_k
        self.v_size_k = v_size_k
        self.h_size = int(self.parent_surface.get_width() * h_size_k)
        if kwargs.get(Attrs.RectSize, False):
            self.v_size = self.h_size
        else:
            self.v_size = int(self.parent_surface.get_height() * v_size_k)

        if x_k is None:
            self.x_k = 0.5 - self.h_size_k / 2
        else:
            self.x_k = 0.00001 if x_k == 0. else x_k

        if y_k is None:
            self.y_k = 0.5 - self.v_size_k / 2
        else:
            self.y_k = 0.00001 if y_k == 0. else y_k

        self.x = self.get_x()
        self.y = self.get_y()

        self.surface_transparent = kwargs.get(Attrs.SurfaceTransparent, UIDefault.SurfaceTransparent)
        self.surface_flags = kwargs.get(Attrs.SurfaceFlags, UIDefault.SurfaceFlags)
        self.surface_color = kwargs.get(Attrs.SurfaceColor, UIDefault.SurfaceColor)
        self.surface = self.get_surface() if build_surface else None
        self.postpone_build = kwargs.get(Attrs.PostponeBuild, False)

    def default_get_x(self) -> int:
        return int(self.x_k * self.parent_surface.get_width())

    def default_get_y(self) -> int:
        return int(self.y_k * self.parent_surface.get_height())

    def default_get_surface(self, h_size=None, v_size=None,
                            transparent=None, color=None,
                            flags=None,
                            fill=True) -> Surface:
        h_size = self.h_size if h_size is None else h_size
        v_size = self.v_size if v_size is None else v_size
        flags = getattr(self, Attrs.SurfaceFlags, UIDefault.SurfaceFlags) if flags is None else flags
        transparent = getattr(self, Attrs.SurfaceTransparent,
                              UIDefault.SurfaceTransparent) if transparent is None else transparent
        surface = get_surface(h_size, v_size,
                              transparent=transparent,
                              flags=flags,
                              )
        if fill:
            self.fill_surface(surface, color)

        return surface

    def default_fill_surface(self, surface: Surface = None, color=None) -> None:
        surface = self.surface if surface is None else surface
        color = color if color else getattr(self, Attrs.SurfaceColor, CommonColors.white)

        surface.fill(color)

    def default_draw(self):
        if self.visible:
            self.parent_surface.blit(self.surface, self.position)

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

    def make_inactive_and_invisible(self) -> None:
        self.deactivate()
        self.visible = 0

    def make_active_and_visible(self) -> None:
        self.activate()
        self.visible = 1

    @property
    def position(self) -> tuple:
        return self.x, self.y

    @property
    def width(self):
        return self.h_size

    @property
    def height(self):
        return self.v_size

    @property
    def size(self) -> tuple[int, int]:
        return self.h_size, self.v_size

    @property
    def real_position(self) -> Vector2DType:
        x, y = self.parent.real_position if self.parent else (0, 0)
        return x + self.x, y + self.y


class UpdateInterface:
    @abstractmethod
    def update(self):
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


class DrawBorder:
    def __init__(self, **kwargs):
        self.border_size = kwargs.get(Attrs.BorderSize, UIDefault.BorderSize)
        self.border_color = kwargs.get(Attrs.BorderColor, UIDefault.BorderColor)
        self.inacborder_color = kwargs.get(Attrs.InacBorderColor, UIDefault.InacBorderColor)

        self.border_radius = kwargs.get(Attrs.BorderRadius, UIDefault.BorderRadius)
        self.border_top_left_radius = kwargs.get(Attrs.BorderTopLeftRadius, UIDefault.BorderTopLeftRadius)
        self.border_top_right_radius = kwargs.get(Attrs.BorderTopRightRadius, UIDefault.BorderTopRightRadius)
        self.border_bottom_left_radius = kwargs.get(Attrs.BorderBottomLeftRadius, UIDefault.BorderBottomLeftRadius)
        self.border_bottom_right_radius = kwargs.get(Attrs.BorderBottomRightRadius, UIDefault.BorderBottomRightRadius)

    @property
    def border_round_attrs(self) -> tuple:
        return self.border_radius, \
               self.border_top_left_radius, self.border_top_right_radius, \
               self.border_bottom_left_radius, self.border_bottom_right_radius

    def draw_border(self: BaseUI, surface=None, color=None, rect=None):
        surface = surface if surface else self.surface
        color = color if color else getattr(self, Attrs.BorderColor, CommonColors.white)
        rect = rect if rect else surface.get_rect()
        draw_rect(surface,
                  color,
                  rect,
                  getattr(self, Attrs.BorderSize, UIDefault.BorderSize),
                  getattr(self, Attrs.BorderRadius, UIDefault.BorderRadius),
                  getattr(self, Attrs.BorderTopLeftRadius, UIDefault.BorderTopLeftRadius),
                  getattr(self, Attrs.BorderTopRightRadius, UIDefault.BorderTopRightRadius),
                  getattr(self, Attrs.BorderBottomLeftRadius, UIDefault.BorderBottomLeftRadius),
                  getattr(self, Attrs.BorderBottomRightRadius, UIDefault.BorderBottomRightRadius),
                  )

    def fill_surface_due_to_border_attrs(self, surface=None, color=None):
        surface = surface if surface else self.surface
        color = color if color else getattr(self, Attrs.SurfaceColor, UIDefault.SurfaceColor)
        draw_rect(
            surface,
            color,
            ((0, 0), surface.get_size()),
            0,
            getattr(self, Attrs.BorderTopLeftRadius, UIDefault.BorderTopLeftRadius),
            getattr(self, Attrs.BorderTopRightRadius, UIDefault.BorderTopRightRadius),
            getattr(self, Attrs.BorderBottomLeftRadius, UIDefault.BorderBottomLeftRadius),
            getattr(self, Attrs.BorderBottomRightRadius, UIDefault.BorderBottomRightRadius),
        )


class BuildRectShapeMixin:
    def get_real_pos(self):
        if self.parent:
            x, y = self.parent.x + self.x, self.parent.y + self.y
        else:
            x, y = self.x, self.y
        return x, y

    def init_rect_shape(self) -> None:
        self.shape = self.shape_class(*self.get_real_pos(), self.h_size, self.v_size)

    def move_rect_shape(self, xy) -> None:
        self.x, self.y = xy
        self.shape.move(xy)

    def reload_shape_position(self):
        self.shape.move(*self.get_real_pos())
