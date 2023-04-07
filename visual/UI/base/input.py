from pygame import Surface

from global_obj.main import Global
from visual.UI.base.text import Text
from settings.visual.ui_default import UIDefault
from visual.UI.base.abs import ShapeAbs
from visual.UI.constants.attrs import Attrs, InputAttr, StyleAttrs
from visual.UI.base.element import BaseUI, GetSurfaceMixin, DrawBorderMixin, BuildRectShapeMixin


class InputBase(BaseUI, DrawBorderMixin, BuildRectShapeMixin, GetSurfaceMixin, ShapeAbs):
    def __init__(self, uid, text='', default_text='', **kwargs):

        super(InputBase, self).__init__(uid=uid, **kwargs)
        DrawBorderMixin.__init__(self)
        ShapeAbs.__init__(self, **kwargs)

        txt_data = kwargs.get(Attrs.TextKwargs, {})
        txt_uid = txt_data.pop(Attrs.UID, f'{self.uid}_txt')
        self.on_enter_action: callable = kwargs.get(InputAttr.OnEnterAction)
        self.on_unfocus_action: callable = kwargs.get(InputAttr.OnUnfocusAction)

        def_text_data = txt_data.copy()
        self.default_text = Text(
            uid=f'def_{txt_uid}',
            text=default_text,
            parent=self,
            auto_draw=False,
            color=kwargs.pop(InputAttr.DefaultTextColor, UIDefault.InacTextColor),
            x_k=def_text_data.pop(Attrs.XK, None),
            y_k=def_text_data.pop(Attrs.YK, None),
            from_left=txt_data.pop(StyleAttrs.FromLeft.value, True),
            **def_text_data.pop(Attrs.TextKwargs, {})
        )

        self.text = Text(
            uid=txt_uid,
            text=text,
            parent=self,
            auto_draw=False,
            x_k=txt_data.pop(Attrs.XK, None),
            y_k=txt_data.pop(Attrs.YK, None),
            from_left=txt_data.pop(StyleAttrs.FromLeft.value, True),
            **txt_data.pop(Attrs.TextKwargs, {})
        )

        self.input_is_active = 0
        self.input_position = -1
        self.build()

        self.del_speed = 0.1
        self.del_delay = 0

    def update(self):
        if self.input_is_active and self.active:
            self.check_for_input()
            if Global.keyboard.ENTER or Global.keyboard.ESC:
                self.unfocus()
                if Global.keyboard.ENTER and self.on_enter_action:
                    self.on_enter_action(self)

            elif Global.keyboard.BACKSPACE and self.text.str_text:
                if Global.clock.time - self.del_delay > self.del_speed:
                    self.del_delay = Global.clock.time
                    new_text = self.text.str_text[:-1]
                    self.text.change_text(new_text)
                    self.render()

    def change_text(self, text: str):
        self.text.str_text = text
        self.render()

    def build(self, **kwargs):
        self.text.build()
        self.default_text.build()
        self.render()
        self.init_shape()

    def render(self, **kwargs):
        self.fill_surface()
        if self.text.str_text:
            self.text.render()
            self.text.draw()
        else:
            self.default_text.render()
            self.default_text.draw()

        self.draw_border()

    def focus(self) -> None:
        self.input_is_active = 1

    def unfocus(self) -> None:
        if self.on_unfocus_action:
            self.on_unfocus_action(self)
        self.input_is_active = 0

    def get_surface(self, **kwargs) -> Surface:
        return self.default_get_surface(**kwargs)

    def fill_surface(self, surface=None, color=None) -> None:
        self.fill_surface_due_to_border_attrs(surface, color)

    def get_x(self) -> int:
        return self.default_get_x()

    def get_y(self):
        return self.default_get_y()

    def check_for_input(self):
        if Global.keyboard.text:
            new_text = self.text.str_text + ''.join(Global.keyboard.text)
            self.text.change_text(new_text)
            self.render()

    def init_shape(self) -> None:
        self.init_rect_shape()

    def move(self, xy):
        self.move_rect_shape(xy)

    def draw(self):
        self.parent_surface.blit(self.surface, self.position)

        if Global.test_draw:
            from pygame.draw import circle
            for d in self.shape.dots:
                circle(self.parent_surface, (255, 255, 255), d, 3)

    @property
    def str_text(self):
        return self.text.str_text
