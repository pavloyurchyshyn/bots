from visual.UI.base.menu import Menu
from game_client.stages.main_menu.settings.menu_abs import MenuAbs
from game_client.stages.maps_editor.settings import map_area
from game_client.stages.maps_editor.settings.map_area import MapRect
from game_client.stages.maps_editor.settings.buttons import BUTTONS_DATA
from core.world.base.constants import TileDataAbs, IMPASSABLE_VALUE, TileTypes, EmptyTile

from core.world.base.visual.world import VisualWorld
from global_obj import Global
from pygame.draw import rect as draw_rect, circle as draw_circle

# Global.stages.map_editor()


class MapEditor(Menu, MenuAbs):
    def __init__(self):
        super(MapEditor, self).__init__(BUTTONS_DATA)
        self.w = VisualWorld(MapRect.rect)
        self.w.init_hex_math()
        self.init_map()

    def init_map(self):
        x_size = int(MapRect.H_size // self.w.hex_math.horizontal_spacing(self.w.tile_size)) - 2
        y_size = int(MapRect.V_size // self.w.hex_math.vertical_spacing(self.w.tile_size)) - 2
        empty_map = [[EmptyTile() for _ in range(x_size)] for _ in range(y_size)]
        self.w.build_map(True, True, empty_map)
        self.define_map_position()

    def update(self):
        self.check_for_drag()
        self.check_for_scale()

    def draw(self):
        Global.display.fill((0, 0, 0))
        self.w.draw()
        draw_rect(Global.display, (255, 255, 255), self.w.window_rect, 3)

        for btn in self.buttons:
            btn.draw()

        self.w.draw_border_under_mouse()
        # pos = self.w.get_mouse_to_xy()
        # if pos in self.w.xy_to_tile:
        #     draw_circle(Global.display, (255, 0, 255),
        #                 self.w.get_normalized_mouse_pos(),
        #                 5)

    def check_for_drag(self):
        if Global.mouse.m_hold:
            self.w.dx += Global.mouse.rel_x
            self.w.dy += Global.mouse.rel_y
            self.define_map_position()

    def check_for_scale(self):
        if scroll := Global.mouse.scroll:
            map_bigger = False
            if self.w.surface.get_width() * 1.02 > MapRect.H_size:
                map_bigger = True
            elif self.w.surface.get_height() * 1.02 > MapRect.V_size:
                map_bigger = True
            # map_bigger = self.w.surface.get_width()*1.02 > MapRect.H_size
            # or
            # self.w.surface.get_height()*1.02 > MapRect.V_size
            if scroll > 0 or (scroll < 0 and map_bigger):
                self.w.scale = self.w.scale + scroll * Global.clock.d_time * 2
                self.w.scale_surface()
                self.define_map_position()

    def define_map_position(self):
        if MapRect.H_size > self.w.surface.get_width():
            self.w.dx = (MapRect.H_size - self.w.surface.get_width()) // 2
        elif self.w.dx > 0:
            self.w.dx = 0
        elif self.w.surface.get_width() + self.w.dx < MapRect.H_size:
            self.w.dx = MapRect.H_size - self.w.surface.get_width()

        if MapRect.V_size > self.w.surface.get_height():
            self.w.dy = (MapRect.V_size - self.w.surface.get_height()) // 2
        elif self.w.dy > 0:
            self.w.dy = 0
        elif self.w.surface.get_height() + self.w.dy < MapRect.V_size:
            self.w.dy = MapRect.V_size - self.w.surface.get_height()
        # TODO leave place between map and borders
