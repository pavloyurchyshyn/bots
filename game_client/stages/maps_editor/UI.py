from typing import List, Tuple
from pygame.draw import rect as draw_rect

from core.world.maps_manager import MapsManager
from core.world.classic_maps.empty import Empty
from core.world.base.visual.world import VisualWorld
from core.world.base.logic.tiles_data import EmptyTile, TileTypes, SpawnTile

from game_client.stages.maps_editor.settings.other import *
from game_client.stages.maps_editor.settings.uids import UIDs
from game_client.stages.maps_editor.settings.menu_abs import MenuAbs
from game_client.stages.maps_editor.settings.buttons import BUTTONS_DATA
from game_client.stages.maps_editor.settings.pencil_buttons import PencilElement
from game_client.stages.maps_editor.chosen_pencil_module import ChosenPencilModule

from visual.UI.base.menu import Menu
from visual.UI.base.text import Text
from visual.UI.base.input import InputBase
from visual.UI.popup_controller import PopUpsController
from visual.UI.base.mixins import DrawElementBorderMixin

from settings.localization.menus.UI import UILocal
from settings.tile_settings import TileSettings


class MapEditor(Menu, PopUpsController, MenuAbs, DrawElementBorderMixin, ChosenPencilModule):
    def __init__(self):
        super(MapEditor, self).__init__({**BUTTONS_DATA})
        PopUpsController.__init__(self)
        ChosenPencilModule.__init__(self)
        self.name_inp = InputBase(UIDs.MapNameInput,
                                  text='',
                                  default_text='Enter name',
                                  x_k=NameInput.X,
                                  y_k=NameInput.Y,
                                  h_size_k=NameInput.H_size,
                                  v_size_k=NameInput.V_size,
                                  surface_color=(100, 100, 100),
                                  parent=self,
                                  from_left=True,
                                  )
        self.size_txt = Text('size',
                             from_left=True,
                             parent=self,
                             font_size=scaled_w(0.009),
                             x_k=0.8, y_k=0.07,
                             h_size_k=0.2, v_size_k=0.1)

        self.w_h_size_txt = Text('h_size',
                                 from_left=True,
                                 parent=self,
                                 font_size=scaled_w(0.009),
                                 x_k=0.8, y_k=0.105,
                                 h_size_k=0.1, v_size_k=0.1,
                                 )
        self.w_v_size_txt = Text('v_size',
                                 from_left=True,
                                 parent=self,
                                 font_size=scaled_w(0.009),
                                 x_k=0.8, y_k=0.14,
                                 h_size_k=0.1, v_size_k=0.1,
                                 )

        self.spawns_amount_txt = Text('spawn_amount',
                                      from_left=True,
                                      parent=self,
                                      font_size=scaled_w(0.009),
                                      x_k=0.8, y_k=0.17,
                                      h_size_k=0.1, v_size_k=0.1,
                                      )

        self.w: VisualWorld = VisualWorld(MapRect.rect, tile_radius=TileSettings.visual_tile_radius)
        self.maps_mngr: MapsManager = MapsManager()
        self.maps_mngr.load_maps()

        self.current_save: MapSave = None

        map_save = None
        if self.maps_mngr.maps:
            map_save = self.maps_mngr.maps[0].copy()
        self.spawns: List[Tuple[int, int]] = None if map_save is None else map_save.spawns
        self.load_save(map_save)

        self.maps_container = Container('maps_container', True,
                                        parent=self,
                                        x_k=MapsButtonsContainer.X, y_k=MapsButtonsContainer.Y,
                                        h_size_k=MapsButtonsContainer.H_size,
                                        v_size_k=MapsButtonsContainer.V_size)
        self.fill_saves_container()

        self.unsaved_edit = False

        self.update_spawns_text()

    def update(self):
        Global.display.fill((0, 0, 0))
        collided_popup_btn = self.update_popups()

        self.size_txt.draw()
        self.w_v_size_txt.draw()
        self.w_h_size_txt.draw()
        self.spawns_amount_txt.draw()
        self.update_and_draw_map()
        self.upd_draw_input()
        self.upd_draw_buttons()

        self.upd_draw_map_container()
        self.update_draw_pencils_container()
        self.draw_pencil_icon()
        self.draw_current_pencil_name()

        self.draw_popups()
        if collided_popup_btn:
            self.draw_border_around_element(collided_popup_btn)

    def load_save(self, map_save: MapSave):
        self.name_inp.change_text(map_save.name)
        self.current_save: MapSave = map_save
        self.spawns = () if map_save is None else map_save.spawns
        self.init_map(map_save)
        self.define_map_position()
        self.update_sizes_texts()
        self.update_spawns_text()

    def fill_saves_container(self):
        self.maps_mngr.load_maps()
        self.maps_container.clear()
        for map_save in self.maps_mngr.maps:
            self.maps_container.add_element(MapFuncUI(uid=map_save.name, map_save=map_save,
                                                      parent=self.maps_container, editor_ui=self), render=False)

        self.maps_container.add_element(MapFuncUI(uid=Empty.name, map_save=Empty(),
                                                  parent=self.maps_container, editor_ui=self), render=False)
        self.maps_container.build()

    def init_map(self, map_save: MapSave):
        x_size = int(MapRect.H_size // self.w.hex_math.horizontal_spacing(self.w.tile_radius)) - 2
        y_size = int(MapRect.V_size // self.w.hex_math.vertical_spacing(self.w.tile_radius)) - 2

        if map_save is None:
            map_tiles_data = [[EmptyTile() for _ in range(x_size)] for _ in range(y_size)]
        else:
            map_tiles_data = map_save.get_tiles_data()

        self.w.build_map(map_tiles_data)
        self.w.adapt_scale_to_win_size()

    def update_sizes_texts(self):
        self.size_txt.change_text(f'{Global.localization.get_text_wloc(UILocal.Match.Size)}:'
                                  f' {self.w.x_size}x{self.w.y_size}'
                                  f'\t-\t{self.w.y_size * self.w.x_size} '
                                  f'{Global.localization.get_text_wloc(UILocal.Match.Tiles)}')
        self.w_v_size_txt.change_text(f'{Global.loc.get_text_wloc(UILocal.Match.Width).capitalize()}: {self.w.x_size}')
        self.w_h_size_txt.change_text(f'{Global.loc.get_text_wloc(UILocal.Match.Height).capitalize()}: {self.w.y_size}')

    def update_spawns_text(self):
        self.spawns_amount_txt.change_text(f'Spawns : {len(self.spawns)}')

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

    def upd_draw_map_container(self):
        self.maps_container.draw()
        if self.maps_container.collide_point(Global.mouse.pos):
            if Global.mouse.scroll:
                self.maps_container.change_dy(Global.mouse.scroll)

            mouse_pos = Global.mouse.pos
            for el in self.maps_container.elements:
                el: MapFuncUI
                if el.collide_point(mouse_pos):
                    if el.load_btn.collide_point(mouse_pos) and el.load_btn.active:
                        self.draw_border_around_element(el.load_btn)
                        if Global.mouse.l_up:
                            el.load_btn.do_action()

                    elif el.delete_btn.collide_point(mouse_pos) and el.delete_btn.active:
                        self.draw_border_around_element(el.delete_btn)
                        if Global.mouse.l_up:
                            el.delete_btn.do_action()

                    self.draw_border_around_element(el)

    def upd_draw_buttons(self):
        for b in self.buttons:
            b.draw()
            if b.active and b.collide_point(Global.mouse.pos):
                self.draw_border_around_element(b)
                if Global.mouse.l_up:
                    b.do_action()

    def upd_draw_input(self):
        self.name_inp.draw()
        if self.name_inp.collide_point(Global.mouse.pos):
            self.draw_border_around_element(self.name_inp)
            if Global.mouse.l_up:
                self.name_inp.focus()
        self.name_inp.update()

    def update_and_draw_map(self):
        """Change tile type under mouse"""
        self.check_for_drag()
        self.check_for_scale()
        if (Global.mouse.l_up or Global.mouse.l_hold) and self.w.window_rect.collidepoint(*Global.mouse.pos):
            if tile := self.w.get_tile_under_mouse():

                if not tile.at_edge:
                    if tile.name == SpawnTile.name:
                        if self.current_pencil_type.name != SpawnTile.name:
                            if tile.xy_id in self.spawns:
                                self.spawns.remove(tile.xy_id)
                            self.update_spawns_text()
                    else:
                        if self.current_pencil_type.name == SpawnTile.name:
                            self.spawns.append(tile.xy_id)
                            self.update_spawns_text()

                    tile.apply_type(self.current_pencil_type)
                    self.w.rerender_tile(tile.xy_id)
                    self.unsaved_edit = True

        self.w.draw()
        draw_rect(Global.display, (255, 255, 255), self.w.window_rect, 3)
        self.w.draw_border_under_mouse()

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

                if scroll > 0 or (scroll < 0 and map_bigger):
                    self.w.set_scale(self.w.scale + scroll * Global.clock.d_time)
                    self.w.reload_surface()
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

    def add_save_h_size_r(self):
        x = self.w.x_size
        self.w.x_size += 1
        for y in range(self.w.y_size):
            self.w.add_tile(self.w.get_tile_from_data(x, y, EmptyTile(), at_edge=True))
            self.w.xy_to_tile[(x - 1, y)].at_edge = (y == 0) or (y == self.w.y_size - 1)

        self.rerender_map()
        self.update_sizes_texts()

    def minus_save_h_size_r(self):
        x = self.w.x_size - 1
        self.w.x_size -= 1
        for y in range(self.w.y_size):
            self.w.remove_tile_by_xy((x, y))
            self.w.xy_to_tile[(self.w.x_size - 1, y)].at_edge = True
            self.w.xy_to_tile[(self.w.x_size - 1, y)].apply_type(EmptyTile)

        self.rerender_map()
        self.update_sizes_texts()

    def add_save_h_size_l(self):
        # TODO
        self.w.x_size += 1
        for tile in self.w.tiles.copy():
            self.w.remove_tile(tile)
            tile.x_id += 1
            self.w.add_tile(tile)
            if tile.x_id == 1:
                tile.at_edge = (tile.y_id == 0) or (tile.y_id == self.w.y_size - 1)

        x = min(self.w.tiles, key=lambda t: t.id_x).x_id - 1
        for y in range(self.w.y_size):
            self.w.add_tile(self.w.get_tile_from_data(x, y, EmptyTile(), at_edge=True))
            # self.w.xy_to_tile[(1, y)].at_edge = (y == 0) or (y == self.w.y_size - 1)

        self.rerender_map()
        self.update_sizes_texts()

    def minus_save_h_size_l(self):
        # TODO
        pass

    def add_save_v_size_b(self):
        y = self.w.y_size
        self.w.y_size += 1
        for x in range(self.w.x_size):
            self.w.add_tile(self.w.get_tile_from_data(x, y, EmptyTile(), at_edge=True))
            self.w.xy_to_tile[(x, y - 1)].at_edge = x in (0, self.w.x_size - 1)

        self.rerender_map()
        self.update_sizes_texts()

    def minus_save_v_size_b(self):
        self.w.y_size -= 1
        y = self.w.y_size
        for x in range(self.w.x_size):
            self.w.remove_tile_by_xy((x, y))
            self.w.xy_to_tile[(x, y - 1)].at_edge = True

        self.rerender_map()
        self.update_sizes_texts()

    def rerender_map(self):
        self.w.render()
        self.w.adapt_scale_to_win_size()
        self.define_map_position()
