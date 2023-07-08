from abc import ABC
from typing import Iterable, Any
from pygame import Surface

from global_obj.main import Global

from visual.UI.base.text import Text
from visual.UI.base.abs import ShapeAbs
from visual.UI.base.style import ButtonStyle
from visual.UI.base.element import BaseUI, GetSurfaceMixin, DrawBorderMixin, BuildRectShapeMixin
from visual.UI.constants.attrs import ButtonAttrs, TextAttrs

from settings.visual.ui_default import UIDefault


class BaseButton(BaseUI, DrawBorderMixin, BuildRectShapeMixin, ShapeAbs, GetSurfaceMixin, ABC):
    style: ButtonStyle
    default_style = ButtonStyle()

    def __init__(self, uid,
                 text,
                 on_click_action: callable = None,
                 inactive_text: str = None,
                 text_uid=None,
                 text_kwargs: dict = None,
                 inactive_text_kwargs: dict = None,
                 **kwargs):
        text_kwargs = text_kwargs if text_kwargs is not None else {}
        inactive_text_kwargs = inactive_text_kwargs if inactive_text_kwargs is not None else {}
        self.clicked = 0
        self.surface = None
        self.inactive_after_click = kwargs.get(ButtonAttrs.InactiveAfterClick, False)
        self.invisible_after_click = kwargs.get(ButtonAttrs.InvisAfterClick, False)

        self.on_click_action: callable = on_click_action
        self.on_click_action_args: Iterable = kwargs.pop(ButtonAttrs.OnClickAction, ())
        self.on_click_action_kwargs: dict = kwargs.pop(ButtonAttrs.OnClickAction, {})
        super(BaseButton, self).__init__(uid=uid, **kwargs)
        ShapeAbs.__init__(self, **kwargs)

        self.active_surface: Surface = self.get_rect_surface(self.h_size, self.v_size,
                                                             transparent=self.style.surface_transparent,
                                                             flags=self.style.surface_flags,
                                                             )
        self.inactive_surface: Surface = self.get_rect_surface(self.h_size, self.v_size,
                                                               transparent=self.style.inac_surface_transparent,
                                                               flags=self.style.inac_surface_flags,
                                                               )

        raw_text_ = kwargs.pop(TextAttrs.RawText, True)
        raw_text = raw_text_ and text_kwargs.pop(TextAttrs.RawText, False)
        self.text = Text(
            text_uid if text_uid else f'{self.uid}_txt',
            text,
            postpone_build=True,
            parent=self,
            auto_draw=True,
            parent_surface=self.active_surface,
            raw_text=raw_text,
            **text_kwargs,
        )

        raw_text = raw_text_ and inactive_text_kwargs.pop(TextAttrs.RawText, False)
        self.inactive_text = Text(
            text_uid if text_uid else f'inac_{self.uid}_txt',
            inactive_text if inactive_text else text,
            postpone_build=True,
            parent=self,
            auto_draw=True,
            parent_surface=self.inactive_surface,
            raw_text=raw_text,
            color=inactive_text_kwargs.pop(TextAttrs.Color, UIDefault.InacTextColor),
            **inactive_text_kwargs,
        )
        if not kwargs.get(ButtonAttrs.PostponeBuild, False):
            self.build()

    def do_action(self, *args, **kwargs) -> Any:
        Global.logger.debug(f'Button "{self.uid}" do action on stage "{Global.stages.current_stage}".')
        Global.music_player.click_sound()
        if self.on_click_action:
            res = self.on_click_action(self, *self.on_click_action_args, *args, **self.on_click_action_kwargs, **kwargs)
        else:
            res = None
        if self.inactive_after_click:
            self.deactivate()
        if self.invisible_after_click:
            self.make_invisible()

        return res

    def switch_active(self) -> None:
        super(BaseButton, self).switch_active()
        self.surface = self.active_surface if self.active else self.inactive_surface

    def set_active(self, state: bool):
        super(BaseButton, self).set_active(state)
        self.surface = self.active_surface if self.active else self.inactive_surface

    def activate(self) -> None:
        super().activate()
        self.surface = self.active_surface

    def deactivate(self) -> None:
        super().deactivate()
        self.surface = self.inactive_surface

    def __str__(self):
        return f'Btn[{self.uid}, {self.x, self.y}]'


class Button(BaseButton):

    def init_shape(self) -> None:
        self.init_rect_shape()

    def draw(self):
        self.default_draw()
        if Global.test_draw and self.shape:
            color = (0, 100, 0) if self.visible and self.active else (100, 0, 0)

            from pygame.draw import circle
            for d in self.shape.dots:
                circle(self.parent_surface, color, d, 3)

    def get_x(self) -> int:
        return int(self.parent_surface.get_width() * self.x_k)

    def get_y(self) -> int:
        return int(self.parent_surface.get_height() * self.y_k)

    def get_surface(self, h_size=None, v_size=None, transparent=None, color=None, flags=None) -> Surface:
        h_size = self.h_size if h_size is None else h_size
        v_size = self.v_size if v_size is None else v_size
        return self.get_rect_surface(h_size, v_size,
                                     transparent=transparent,
                                     flags=flags,
                                     color=color,
                                     )

    def fill_surface(self, surface: Surface = None, color=None) -> None:
        self.fill_surface_due_to_border_attrs(surface, color)

    def build(self) -> 'self':
        self.render()
        self.init_shape()
        return self

    def render(self):
        self.fill_surface(surface=self.active_surface, color=self.style.surface_color)
        self.text.render()
        self.text.draw()
        self.draw_border(self.active_surface, self.style.border_color)

        self.fill_surface(self.inactive_surface, self.style.inac_surface_color)
        self.inactive_text.render()
        self.inactive_text.draw()
        self.draw_border(self.inactive_surface, self.style.inacborder_color)

        self.surface = self.active_surface if self.active else self.inactive_surface

    def move(self, xy) -> None:
        self.move_rect_shape(xy)
