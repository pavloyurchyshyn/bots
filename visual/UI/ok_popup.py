from pygame import Surface
from global_obj import Global

from visual.UI.base.button import Button
from visual.UI.base.pop_up import PopUpBase
from visual.UI.constants.attrs import Attrs
from settings.localization.menus.common import CommonText
from game_client.stages.styles import get_default_btn_style


class OkPopUp(PopUpBase):
    def init_shape(self) -> None:
        self.init_rect_shape()

    def __init__(self, uid, ok_uid=None, on_click_action=None, **kwargs):
        super(OkPopUp, self).__init__(uid=uid, **kwargs)
        self.on_click_action = on_click_action
        ok_uid = ok_uid if ok_uid else f'{self.uid}_ok_btn'
        button_data = kwargs.pop(Attrs.ButtonKwargs, {})
        button_data[Attrs.Style] = button_data.get(Attrs.Style, get_default_btn_style())
        button_data[Attrs.HSizeK] = button_data.get(Attrs.HSizeK, 0.4)
        button_data[Attrs.VSizeK] = button_data.get(Attrs.VSizeK, 0.25)
        button_data[Attrs.YK] = button_data.get(Attrs.YK, 1 - button_data[Attrs.VSizeK]*1.1)
        self.ok = Button(uid=ok_uid,
                         parent=self,
                         on_click_action=self.close,
                         text=CommonText.Ok,
                         postpone_build=True,
                         **button_data,
                         )
        self.buttons.append(self.ok)
        self.build()

    def close(self, b: Button):
        self.make_inactive_and_invisible()

    def draw(self):
        self.parent_surface.blit(self.surface, self.position)
        self.parent_surface.blit(self.ok.surface, (self.x + self.ok.x, self.y + self.ok.y))

    def get_x(self) -> int:
        return self.default_get_x()

    def get_y(self) -> int:
        return self.default_get_y()

    def build(self, **kwargs):
        self.render()
        self.init_rect_shape()

    def render(self, **kwargs):
        self.fill_surface_due_to_border_attrs()
        self.text.render()
        self.text.draw()
        self.draw_border()
        self.ok.render()
        self.ok.build()

    def move(self, xy):
        raise NotImplementedError

    def get_surface(self, **kwargs) -> Surface:
        return self.get_rect_surface(self.h_size, self.v_size,
                                     transparent=self.style.surface_transparent,
                                     flags=self.style.surface_flags, )

    def fill_surface(self, surface=None, color=None) -> None:
        self.fill_surface_due_to_border_attrs()

    def update(self):
        if Global.mouse.l_up:
            if self.ok.collide_point(Global.mouse.pos):
                self.ok.do_action()
                if self.on_click_action:
                    self.on_click_action(self, self.ok)
