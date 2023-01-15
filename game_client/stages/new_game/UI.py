from math import cos
from pygame.draw import rect as draw_rect

from global_obj.main import Global

from visual.UI.base.menu import Menu
from visual.UI.settings import UIDefault
from visual.UI.base.button import Button

from game_client.stages.new_game.settings.buttons import BUTTONS_DATA
from game_client.stages.new_game.settings.menu_abs import NewGameAbs


class NewGame(Menu, NewGameAbs):
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
        r_c = UIDefault.CollidedElBorder.r_0 + UIDefault.CollidedElBorder.r_1 * abs(cos(Global.clock.time))
        g_c = UIDefault.CollidedElBorder.g_0 + UIDefault.CollidedElBorder.g_1 * abs(cos(Global.clock.time))
        b_c = UIDefault.CollidedElBorder.b_0 + UIDefault.CollidedElBorder.b_1 * abs(cos(Global.clock.time))
        draw_rect(Global.display, (r_c, g_c, b_c), element.shape.get_rect(), 2, *element.border_round_attrs)
