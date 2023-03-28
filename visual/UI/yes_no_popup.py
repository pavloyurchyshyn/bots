from pygame import Surface
from global_obj.main import Global

from visual.UI.base.button import Button
from visual.UI.base.pop_up import PopUpBase
from visual.UI.constants.attrs import Attrs
from settings.localization.menus.common import CommonText
from visual.styles import get_btn_style


class YesNoPopUp(PopUpBase):

    def init_shape(self) -> None:
        self.init_rect_shape()

    def __init__(self, uid,
                 text: str,
                 yes_uid=None, no_uid=None,
                 yes_text=CommonText.Yes,
                 yes_btn_xk=None, yes_btn_yk=None,
                 yes_btn_hk=0.4, yes_btn_vk=0.25,
                 no_text=CommonText.No,
                 no_btn_xk=None, no_btn_yk=None,
                 no_btn_hk=0.4, no_btn_vk=0.25,
                 on_click_action=None,
                 yes_on_click_action=None,
                 no_on_click_action=None,
                 **kwargs):
        super(YesNoPopUp, self).__init__(uid=uid, text=text, **kwargs)
        self.on_click_action = on_click_action

        button_data = kwargs.pop(Attrs.ButtonKwargs, {})
        button_data[Attrs.Style] = button_data.get(Attrs.Style, get_btn_style())

        yes_uid = yes_uid if yes_uid else f'{self.uid}_yes_btn'
        no_uid = no_uid if no_uid else f'{self.uid}_no_btn'

        yes_btn_xk = yes_btn_xk if yes_btn_xk else (1 - yes_btn_hk - no_btn_hk) / 3
        yes_btn_yk = yes_btn_yk if yes_btn_yk is not None else 1 - yes_btn_vk*1.1

        no_btn_xk = no_btn_xk if no_btn_xk else (1 - yes_btn_hk - no_btn_hk) / 1.5 + yes_btn_hk
        no_btn_yk = no_btn_yk if no_btn_yk is not None else 1 - no_btn_vk*1.1

        self.yes = Button(uid=yes_uid,
                          x_k=yes_btn_xk,
                          y_k=yes_btn_yk,
                          h_size_k=yes_btn_hk,
                          v_size_k=yes_btn_vk,
                          parent=self,
                          on_click_action=yes_on_click_action,
                          text=yes_text,
                          postpone_build=True,
                          **button_data,
                          )
        self.no = Button(uid=no_uid,
                         x_k=no_btn_xk,
                         y_k=no_btn_yk,
                         h_size_k=no_btn_hk,
                         v_size_k=no_btn_vk,
                         parent=self,
                         on_click_action=no_on_click_action,
                         text=no_text,
                         postpone_build=True,
                         **button_data,
                         )

        self.buttons.append(self.yes)
        self.buttons.append(self.no)
        if not kwargs.get(Attrs.PostponeBuild):
            self.build()

    def close(self, button: Button):
        self.make_inactive_and_invisible()

    def draw(self):
        self.parent_surface.blit(self.surface, self.position)
        self.parent_surface.blit(self.yes.surface, (self.x + self.yes.x, self.y + self.yes.y))
        self.parent_surface.blit(self.no.surface, (self.x + self.no.x, self.y + self.no.y))

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
        self.yes.build()
        self.no.build()

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
            if self.yes.collide_point(Global.mouse.pos):
                self.yes.do_action()
                if self.on_click_action:
                    self.on_click_action(self, self.yes)
            elif self.no.collide_point(Global.mouse.pos):
                self.no.do_action()
                if self.on_click_action:
                    self.on_click_action(self, self.no)

    def on_enter_action(self):
        self.yes.do_action()