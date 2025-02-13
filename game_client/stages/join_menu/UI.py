from visual.UI.base.menu import Menu
from game_client.stages.maps_editor.settings.menu_abs import MenuAbs
from global_obj.main import Global

from game_client.stages.join_menu.settings.buttons import BUTTONS_DATA
from visual.UI.base.mixins import DrawElementBorderMixin
from visual.UI.popup_controller import PopUpsController


class JoinMenu(Menu, PopUpsController, MenuAbs, DrawElementBorderMixin):
    def __init__(self):
        super(JoinMenu, self).__init__(BUTTONS_DATA)
        PopUpsController.__init__(self)
        pass

    def update(self):
        Global.display.fill((0, 0, 0))
        for b in self.buttons:
            b.draw()
            if b.active and b.collide_point(Global.mouse.pos):
                self.draw_border_around_element(b)
                if Global.mouse.l_up:
                    b.do_action()
