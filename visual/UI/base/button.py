from typing import Iterable, Any
from visual.UI.base.element import BaseUI, GetSurfaceMixin, DrawBorderMixin
from visual.UI.base.text import Text
from visual.UI.constants.attrs import Attrs
from core.shape import Rectangle, Circle
from visual.UI.settings import UIDefault


class BaseButton(BaseUI, GetSurfaceMixin, DrawBorderMixin):
    def __init__(self, uid,
                 text,
                 on_click_action: callable,
                 text_uid=None,
                 text_kwargs: dict = None,
                 **kwargs):
        text_kwargs = text_kwargs if text_kwargs is not None else {}

        self.on_click_action: callable = on_click_action
        self.on_click_action_args: Iterable = kwargs.pop(Attrs.OnClickAction, ())
        self.on_click_action_kwargs: dict = kwargs.pop(Attrs.OnClickAction, {})
        self.border_size = kwargs.get(Attrs.BorderSize, UIDefault.BorderSize)
        self.border_color = kwargs.get(Attrs.BorderColor, UIDefault.BorderColor)

        super(BaseButton, self).__init__(uid=uid,
                                         **kwargs)

        self.text = Text(
            text_uid if text_uid else f'{text_uid}_txt',
            text,
            parent=self,
            auto_draw=True,
            **text_kwargs,
        )
        self.text.build()
        self.draw_border()

    def do_action(self) -> Any:
        return self.on_click_action(self, *self.on_click_action_args, **self.on_click_action_kwargs)


class Button(BaseButton):
    def init_shape(self) -> None:
        self.shape = self.shape_class(self.x, self.y, self.h_size, self.v_size)

    def build_position(self) -> None:
        self.default_build_position()

    def render(self):
        self.surface = self.get_rect_surface(self.h_size, self.v_size)

    def move(self, xy):
        self.x, self.y = xy
        self.shape.move(xy)
