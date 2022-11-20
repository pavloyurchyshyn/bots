from math import cos
from pygame.draw import rect as draw_rect
from global_obj import Global
from visual.UI.base.menu import Menu
from visual.UI.base.button import Button
from game.stages.main_menu.settings.buttons import BUTTONS_DATA, MenuAbs


class MainMenu(Menu, MenuAbs):
    def __init__(self):
        super().__init__(BUTTONS_DATA)

    def update(self):
        for b in self.buttons:
            b.draw()
            if b.active and b.collide_point(Global.mouse.pos):
                self.draw_border(b)
                if Global.mouse.l_up:
                    b.do_action()

    def draw_border(self, element: Button):
        # color = 256 * abs(cos(Global.clock.time))
        r_c = 155 + 100 * abs(cos(Global.clock.time))
        g_c = 115 + 100 * abs(cos(Global.clock.time))
        b_c = 50 * abs(cos(Global.clock.time))
        draw_rect(Global.display, (r_c, g_c, b_c), element.shape.get_rect(), 2)
