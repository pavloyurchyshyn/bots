from visual.UI.base.menu import Menu
from game_client.stages.maps_editor.settings.menu_abs import MenuAbs

from core.world.base.constants import EmptyTile

from core.world.base.visual.world import VisualWorld
from global_obj import Global
from pygame.draw import rect as draw_rect

from visual.UI.base.input import InputBase
from visual.UI.base.container import Container
from game_client.stages.maps_editor.settings.other import *
from game_client.stages.maps_editor.settings.buttons import BUTTONS_DATA
from game_client.stages.maps_editor.settings.uids import UIDs
from core.world.maps_manager import MapsManager
from visual.UI.base.mixins import DrawElementBorderMixin


class MapEditor(Menu, MenuAbs, DrawElementBorderMixin):
    def __init__(self):
        super(MapEditor, self).__init__(BUTTONS_DATA)
        self.w = VisualWorld(MapRect.rect)
        self.maps_mngr = MapsManager()
        self.w.init_hex_math()
        map_to_init = None
        if self.maps_mngr.maps:
            map_to_init = self.maps_mngr.maps[0]
        self.init_map(map_to_init.get_tiles_data())

        self.name_inp = InputBase(UIDs.MapNameInput,
                                  text=map_to_init.name if map_to_init else '',
                                  default_text='Enter name',
                                  x_k=NameInput.X,
                                  y_k=NameInput.Y,
                                  h_size_k=NameInput.H_size,
                                  v_size_k=NameInput.V_size,
                                  surface_color=(100, 100, 100),
                                  parent=self,
                                  from_left=True,
                                  )

        self.maps_cont = Container('container', True,
                                   parent=self,
                                   x_k=MapsButtonsContainer.X, y_k=MapsButtonsContainer.Y,
                                   h_size_k=MapsButtonsContainer.H_size, v_size_k=MapsButtonsContainer.V_size)
        self.maps_cont.build()
        for map_save in self.maps_mngr.maps:
            self.maps_cont.add_element(MapFuncUI(uid=map_save.name, map_name=map_save.name,
                                                 parent=self.maps_cont, can_be_deleted=map_save.can_be_deleted))

    def init_map(self, map_json_data=None):
        x_size = int(MapRect.H_size // self.w.hex_math.horizontal_spacing(self.w.tile_size)) - 2
        y_size = int(MapRect.V_size // self.w.hex_math.vertical_spacing(self.w.tile_size)) - 2
        if map_json_data is None:
            map_json_data = [[EmptyTile() for _ in range(x_size)] for _ in range(y_size)]
        self.w.build_map(True, True, map_json_data)
        self.define_map_position()

    def update(self):
        self.check_for_drag()
        self.check_for_scale()
        if Global.mouse.l_up and self.name_inp.collide_point(Global.mouse.pos):
            self.name_inp.focus()
        self.name_inp.update()

        for b in self.buttons:
            b.draw()
            if b.active and b.collide_point(Global.mouse.pos):
                self.draw_border_around_element(b)
                if Global.mouse.l_up:
                    b.do_action()

    def draw(self):
        Global.display.fill((0, 0, 0))
        self.w.draw()
        draw_rect(Global.display, (255, 255, 255), self.w.window_rect, 3)

        for btn in self.buttons:
            btn.draw()

        self.maps_cont.draw()
        self.name_inp.draw()
        self.w.draw_border_under_mouse()
        if Global.mouse.l_hold:
            if tile := self.w.get_tile_under_mouse():
                tile.apply_type('forest')
                self.w.rerender_tile((tile.id_x, tile.id_y))

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
            if self.w.window_rect.collidepoint(*Global.mouse.pos):
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
                    self.w.reload_surface()
                    self.define_map_position()
            elif self.maps_cont.collide_point(Global.mouse.pos):
                self.maps_cont.dy += scroll * 4
                self.maps_cont.calculate_elements_position()
                self.maps_cont.render()

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
