from typing import Iterable, Any
from pygame import Surface
from visual.UI.base.element import BaseUI, GetSurfaceMixin, DrawBorderMixin
from visual.UI.base.text import Text
from visual.UI.constants.attrs import Attrs
from core.shape import Circle
from visual.UI.settings import UIDefault


class BaseButton(BaseUI, GetSurfaceMixin, DrawBorderMixin):
    def __init__(self, uid,
                 text,
                 on_click_action: callable,
                 inactive_text: str = None,

                 text_uid=None,
                 text_kwargs: dict = None,
                 inactive_text_kwargs: dict = None,
                 **kwargs):
        text_kwargs = text_kwargs if text_kwargs is not None else {}
        inactive_text_kwargs = inactive_text_kwargs if inactive_text_kwargs is not None else {}
        self.surface = None
        self.active_surface: Surface = None
        self.inactive_surface: Surface = None

        self.on_click_action: callable = on_click_action
        self.on_click_action_args: Iterable = kwargs.pop(Attrs.OnClickAction, ())
        self.on_click_action_kwargs: dict = kwargs.pop(Attrs.OnClickAction, {})
        self.border_size = kwargs.get(Attrs.BorderSize, UIDefault.BorderSize)
        self.border_color = kwargs.get(Attrs.BorderColor, UIDefault.BorderColor)
        self.inac_border_color = kwargs.get(Attrs.InacBorderColor, UIDefault.InacBorderColor)

        super(BaseButton, self).__init__(uid=uid, **kwargs)

        raw_text_ = kwargs.pop(Attrs.RawText, True)
        raw_text = raw_text_ and text_kwargs.pop(Attrs.RawText, True)
        self.text = Text(
            text_uid if text_uid else f'{self.uid}_txt',
            text,
            parent=self,
            auto_draw=True,
            parent_surface=self.active_surface,
            raw_text=raw_text,
            **text_kwargs,
        )

        raw_text = raw_text_ and inactive_text_kwargs.pop(Attrs.RawText, True)
        self.inactive_text = Text(
            text_uid if text_uid else f'inac_{self.uid}_txt',
            inactive_text if inactive_text else text,
            parent=self,
            auto_draw=True,
            parent_surface=self.inactive_surface,
            raw_text=raw_text,
            color=inactive_text_kwargs.pop(Attrs.Color, UIDefault.InacTextColor),
            **inactive_text_kwargs,
        )

    def do_action(self) -> Any:
        return self.on_click_action(self, *self.on_click_action_args, **self.on_click_action_kwargs)

    def switch_active(self) -> None:
        super(BaseButton, self).switch_active()
        self.surface = self.active_surface if self.active else self.inactive_surface

    def activate(self) -> None:
        super().activate()
        self.surface = self.active_surface

    def deactivate(self) -> None:
        super().deactivate()
        self.surface = self.inactive_surface


class Button(BaseButton):
    def init_shape(self) -> None:
        x, y = self.parent.x + self.x, self.parent.y + self.y
        self.shape = self.shape_class(x, y, self.h_size, self.v_size)

    def build_position(self) -> None:
        self.default_build_position()

    def build(self) -> None:
        super(Button, self).build()
        self.draw_border(self.active_surface, self.border_color)
        self.draw_border(self.inactive_surface, self.inac_border_color)

    def render(self):
        self.active_surface = self.get_rect_surface(self.h_size, self.v_size)
        self.inactive_surface = self.get_rect_surface(self.h_size, self.v_size)

        self.surface = self.active_surface if self.active else self.inactive_surface

    def move(self, xy):
        self.x, self.y = xy
        self.shape.move(xy)
