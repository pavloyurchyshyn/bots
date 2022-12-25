from visual.UI.base.menu import Menu
from game_client.stages.main_menu.settings.menu_abs import MenuAbs
from game_client.stages.maps_editor.settings import *
from core.world.base.visual.world import VisualWorld
from settings.tile_settings import TileSettings


class MapEditor:
    def __init__(self):
        super(MapEditor, self).__init__()
        self.w = VisualWorld(10, 10, 500, 500, True, True)

    def update(self):
        pass
