from visual.UI.base.menu import Menu
from game_client.stages.maps_editor.settings.menu_abs import MenuAbs

# from core.world.base.logic.tiles_data import EmptyTile
from core.world.base.map_save import MapSave
# from core.world.base.visual.world import VisualWorld
from global_obj import Global
from pygame.draw import rect as draw_rect
#
# from visual.UI.base.input import InputBase
# from visual.UI.base.container import Container
# from game_client.stages.maps_editor.settings.other import *
from game_client.stages.setup_menu.settings.buttons import BUTTONS_DATA
from game_client.stages.setup_menu.settings.map_elements import MapRect
# from game_client.stages.maps_editor.settings.pencil_buttons import PENCIL_BUTTONS
# from game_client.stages.maps_editor.settings.uids import UIDs
from core.world.maps_manager import MapsManager
from visual.UI.base.mixins import DrawElementBorderMixin
from visual.UI.base.pop_up import PopUpsController
# from visual.UI.base.text import Text
from core.world.base.visual.world import VisualWorld
# TODO clear

class SetupMenu(Menu, PopUpsController, MenuAbs, DrawElementBorderMixin):
    def __init__(self):
        super(SetupMenu, self).__init__(BUTTONS_DATA)
        PopUpsController.__init__(self)
        self.w: VisualWorld = VisualWorld(MapRect.rect)
        self.maps_mngr: MapsManager = MapsManager()
        self.maps_mngr.load_maps()
        self.current_save: MapSave = None

    def update(self):
        Global.display.fill((0, 0, 0))
        self.update_and_draw_map()
        for b in self.buttons:
            b.draw()
            if b.active and b.collide_point(Global.mouse.pos):
                self.draw_border_around_element(b)
                if Global.mouse.l_up:
                    b.do_action()

    def load_save(self, save: MapSave):
        self.current_save = save
        self.w.build_map_from_save(save)
        self.w.adapt_scale_to_win_size()

    def update_and_draw_map(self):
        self.w.draw()
        draw_rect(Global.display, (255, 255, 255), self.w.window_rect, 3)
