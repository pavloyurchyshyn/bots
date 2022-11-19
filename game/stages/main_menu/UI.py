from global_obj import Global
from visual.UI.base.menu import Menu
from game.stages.main_menu.settings.buttons import BUTTONS_DATA


class MainMenu(Menu):
    def __init__(self):
        super().__init__(BUTTONS_DATA)

    def update(self):
        for b in self.buttons:
            if Global.mouse.l_up and b.collide_point(Global.mouse.pos):
                b.do_action()
            b.draw()
