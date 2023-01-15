from abc import abstractmethod, ABC
from pygame import Surface, SRCALPHA
from pygame.draw import rect as draw_rect

from global_obj.main import Global
from core.shape.constants import Vector2DType

from visual.UI.utils import get_surface
from visual.UI.base.style import Style
from visual.UI.base.abs import BaseUIAbs
from visual.UI.settings import UIDefault
from visual.UI.constants.attrs import Attrs, StyleAttrs


class BaseUI(BaseUIAbs, ABC):
    default_style = Style()

    def __init__(self, uid,
                 x_k=None, y_k=None,
                 h_size_k=1, v_size_k=1,
                 parent: BaseUIAbs = None,
                 parent_surface=None,
                 build_surface=True,
                 style: Style = None,
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

        self.style: Style = self.default_style if style is None else style

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

        self.surface = self.get_surface() if build_surface else None

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
        flags = self.style.dict.get(StyleAttrs.SurfaceFlags.value, UIDefault.SurfaceFlags) if flags is None else flags
        if transparent is None:
            transparent = self.style.dict.get(StyleAttrs.SurfaceTransparent.value, UIDefault.SurfaceTransparent)

        surface = get_surface(h_size, v_size,
                              transparent=transparent,
                              flags=flags,
                              )
        if fill:
            self.fill_surface(surface, color)

        return surface

    def default_fill_surface(self, surface: Surface = None, color=None) -> None:
        surface = self.surface if surface is None else surface
        color = color if color else self.style.dict.get(StyleAttrs.SurfaceColor.value, self.Colors.white)

        surface.fill(color)

    def default_draw(self):
        if self.visible:
            self.parent_surface.blit(self.surface, self.position)

    def set_active(self, state: bool):
        self.active = state

    def switch_active(self):
        self.active = not self.active

    def deactivate(self) -> None:
        self.active = 0

    def activate(self) -> None:
        self.active = 1

    @property
    def inactive(self) -> bool:
        return not self.active

    def make_visible(self) -> None:
        self.visible = 1

    def make_invisible(self) -> None:
        self.visible = 0

    @property
    def invisible(self) -> bool:
        return not self.visible

    def make_inactive_and_invisible(self) -> None:
        self.deactivate()
        self.make_invisible()

    def make_active_and_visible(self) -> None:
        self.activate()
        self.make_visible()

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


class GetSurfaceMixin:
    style: Style

    def get_rect_surface(self, h_size, v_size=None, transparent=None, color=None, flags=None):
        flags = flags if flags is not None else self.style.dict.get(StyleAttrs.SurfaceFlags.value, SRCALPHA)
        transparent = transparent if transparent is not None else self.style.dict.get(
            StyleAttrs.SurfaceTransparent.value, 0)
        return get_surface(h_size, v_size,
                           transparent=transparent,
                           flags=flags,
                           color=color,
                           )


class DrawBorderMixin:
    style: Style

    @property
    def border_round_attrs(self) -> tuple:
        return self.style.border_radius, \
               self.style.border_top_left_radius, self.style.border_top_right_radius, \
               self.style.border_bottom_left_radius, self.style.border_bottom_right_radius

    def draw_border(self: BaseUI, surface=None, color=None, rect=None):
        surface = surface if surface else self.surface
        color = color if color else self.style.dict.get(StyleAttrs.BorderColor.value, self.Colors.white)
        rect = rect if rect else surface.get_rect()
        draw_rect(surface,
                  color,
                  rect,
                  self.style.dict.get(StyleAttrs.BorderSize.value, UIDefault.BorderSize),
                  self.style.dict.get(StyleAttrs.BorderRadius.value, UIDefault.BorderRadius),
                  self.style.dict.get(StyleAttrs.BorderTopLeftRadius.value, UIDefault.BorderTopLeftRadius),
                  self.style.dict.get(StyleAttrs.BorderTopRightRadius.value, UIDefault.BorderTopRightRadius),
                  self.style.dict.get(StyleAttrs.BorderBottomLeftRadius.value, UIDefault.BorderBottomLeftRadius),
                  self.style.dict.get(StyleAttrs.BorderBottomRightRadius.value, UIDefault.BorderBottomRightRadius),
                  )

    def fill_surface_due_to_border_attrs(self, surface: Surface = None, color: tuple = None, rect=None):
        surface = surface if surface else self.surface
        color = color if color else self.style.dict.get(StyleAttrs.SurfaceColor.value, UIDefault.SurfaceColor)
        rect = rect if rect else surface.get_rect()

        draw_rect(surface,
                  color,
                  rect,
                  0,
                  self.style.dict.get(StyleAttrs.BorderRadius.value, UIDefault.BorderRadius),
                  self.style.dict.get(StyleAttrs.BorderTopLeftRadius.value, UIDefault.BorderTopLeftRadius),
                  self.style.dict.get(StyleAttrs.BorderTopRightRadius.value, UIDefault.BorderTopRightRadius),
                  self.style.dict.get(StyleAttrs.BorderBottomLeftRadius.value, UIDefault.BorderBottomLeftRadius),
                  self.style.dict.get(StyleAttrs.BorderBottomRightRadius.value, UIDefault.BorderBottomRightRadius),
                  )


class BuildRectShapeMixin:
    def get_real_pos(self):
        if self.parent:
            px, py = self.parent.real_position
            x, y = px + self.x, py + self.y
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
