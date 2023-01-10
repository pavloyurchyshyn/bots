from math import cos
from pygame.draw import rect as draw_rect

from global_obj import Global

from visual.UI.base.menu import Menu
from visual.UI.settings import UIDefault
from visual.UI.base.button import Button
from visual.UI.base.pop_up import PopUpsController

from game_client.stages.main_menu.settings.buttons import BUTTONS_DATA
from game_client.stages.main_menu.settings.menu_abs import MenuAbs
from visual.UI.base.mixins import DrawElementBorderMixin


class MainMenu(Menu, PopUpsController, MenuAbs, DrawElementBorderMixin):
    def __init__(self):
        super().__init__(BUTTONS_DATA)
        PopUpsController.__init__(self)

    def update(self):
        Global.display.fill((0, 0, 0))
        collided_popup_btn = self.update_popups()

        for b in self.buttons:
            b.draw()
            if b.active and b.collide_point(Global.mouse.pos):
                self.draw_border(b)
                if Global.mouse.l_up:
                    b.do_action()

        self.draw_popups()
        if collided_popup_btn:
            self.draw_border_around_element(collided_popup_btn)

    def draw_border(self, element: Button):
        r_c = UIDefault.CollidedElBorder.r_0 + UIDefault.CollidedElBorder.r_1 * abs(cos(Global.clock.time))
        g_c = UIDefault.CollidedElBorder.g_0 + UIDefault.CollidedElBorder.g_1 * abs(cos(Global.clock.time))
        b_c = UIDefault.CollidedElBorder.b_0 + UIDefault.CollidedElBorder.b_1 * abs(cos(Global.clock.time))
        draw_rect(Global.display, (r_c, g_c, b_c), element.shape.get_rect(), 2, *element.border_round_attrs)

    def update_popups(self):
        collided_popup_btn = None
        if self.popups:
            if self.popups[0].collide_point(Global.mouse.pos):
                for btn in self.popups[0].buttons:
                    if btn.collide_point(Global.mouse.pos):
                        collided_popup_btn = btn
                        if Global.mouse.l_up:
                            btn.do_action()
                            if self.popups[0].on_click_action:
                                self.popups[0].on_click_action(self.popups[0], btn)
                            break
                if self.popups and self.popups[0].inactive:
                    self.popups.remove(self.popups[0])
            Global.mouse.l_up = False
            Global.mouse._pos = -10, -10
        return collided_popup_btn
