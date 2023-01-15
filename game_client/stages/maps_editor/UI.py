from visual.UI.base.menu import Menu
from game_client.stages.maps_editor.settings.menu_abs import MenuAbs

from core.world.base.logic.tiles_data import EmptyTile
from core.world.base.map_save import MapSave
from core.world.base.visual.world import VisualWorld
from global_obj.main import Global
from pygame.draw import rect as draw_rect
from core.world.classic_maps.empty import Empty

from visual.UI.base.input import InputBase
from visual.UI.base.container import Container
from game_client.stages.maps_editor.settings.other import *
from game_client.stages.maps_editor.settings.buttons import BUTTONS_DATA
from game_client.stages.maps_editor.settings.pencil_buttons import PENCIL_BUTTONS
from game_client.stages.maps_editor.settings.uids import UIDs
from core.world.maps_manager import MapsManager
from visual.UI.base.mixins import DrawElementBorderMixin
from visual.UI.base.pop_up import PopUpsController
from visual.UI.base.text import Text


class MapEditor(Menu, PopUpsController, MenuAbs, DrawElementBorderMixin):
    def __init__(self):
        super(MapEditor, self).__init__({**BUTTONS_DATA, **PENCIL_BUTTONS})
        PopUpsController.__init__(self)
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
        self.size_txt = Text('', from_left=True, parent=self,
                             x_k=0.802, y_k=0.07, h_size_k=0.1, v_size_k=0.1)

        self.w: VisualWorld = VisualWorld(MapRect.rect)
        self.maps_mngr: MapsManager = MapsManager()
        self.maps_mngr.load_maps()

        self.current_save: MapSave = None

        self.w.init_hex_math()
        map_save = None
        if self.maps_mngr.maps:
            map_save = self.maps_mngr.maps[0].copy()
        self.load_save(map_save)

        self.maps_cont = Container('container', True,
                                   parent=self,
                                   x_k=MapsButtonsContainer.X, y_k=MapsButtonsContainer.Y,
                                   h_size_k=MapsButtonsContainer.H_size,
                                   v_size_k=MapsButtonsContainer.V_size)
        self.fill_container()

        self.unsaved_edit = False

        self.current_pencil_type = 'forest'

    def load_save(self, map_save: MapSave):
        self.name_inp.change_text(map_save.name)
        self.current_save: MapSave = map_save
        self.init_map(map_save, )

    def fill_container(self):
        self.maps_mngr.load_maps()
        self.maps_cont.clear()
        for map_save in self.maps_mngr.maps:
            self.maps_cont.add_element(MapFuncUI(uid=map_save.name, map_save=map_save,
                                                 parent=self.maps_cont, editor_ui=self))

        self.maps_cont.add_element(MapFuncUI(uid=Empty.name, map_save=Empty(),
                                             parent=self.maps_cont, editor_ui=self))
        self.maps_cont.build()

    def init_map(self, map_save: MapSave):
        x_size = int(MapRect.H_size // self.w.hex_math.horizontal_spacing(self.w.tile_size)) - 2
        y_size = int(MapRect.V_size // self.w.hex_math.vertical_spacing(self.w.tile_size)) - 2

        if map_save is None:
            odd = True
            flat = True
            map_tiles_data = [[EmptyTile() for _ in range(x_size)] for _ in range(y_size)]
        else:
            odd = map_save.odd
            flat = map_save.flat
            map_tiles_data = map_save.get_tiles_data()

        self.w.build_map(flat, odd, map_tiles_data)
        self.w.adapt_scale_to_win_size()

        self.define_map_position()
        self.size_txt.change_text(f'{self.w.x_size}X{self.w.y_size}   {self.w.y_size * self.w.x_size}')

    def update(self):
        Global.display.fill((0, 0, 0))
        collided_popup_btn = self.update_popups()

        self.size_txt.draw()
        self.update_and_draw_map()
        self.upd_draw_input()
        self.upd_draw_buttons()
        self.update_and_draw_map()
        self.upd_draw_map_container()

        self.draw_popups()
        if collided_popup_btn:
            self.draw_border_around_element(collided_popup_btn)

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
        self.maps_cont.draw()
        if self.maps_cont.collide_point(Global.mouse.pos):
            if Global.mouse.scroll:
                self.maps_cont.change_dx(Global.mouse.scroll)

            mouse_pos = Global.mouse.pos
            for el in self.maps_cont.elements:
                if el.collide_point(mouse_pos):
                    if el.load_btn.collide_point(mouse_pos) and el.load_btn.active:
                        self.draw_border_around_element(el.load_btn)
                        if Global.mouse.l_up:
                            el.load_btn.do_action()
                            el: MapFuncUI
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
        self.check_for_drag()
        self.check_for_scale()
        if Global.mouse.l_hold:
            if tile := self.w.get_tile_under_mouse():
                tile.apply_type(self.current_pencil_type)
                self.w.rerender_tile((tile.id_x, tile.id_y))
                self.unsaved_edit = True

        self.w.draw()
        draw_rect(Global.display, (255, 255, 255), self.w.window_rect, 3)
        self.w.draw_border_under_mouse()

    # def draw(self):
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

                if scroll > 0 or (scroll < 0 and map_bigger):
                    self.w.scale = self.w.scale + scroll * Global.clock.d_time * 2
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
        # TODO leave place between map and borders
