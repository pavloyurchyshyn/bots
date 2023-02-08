from pygame.draw import rect as draw_rect

from global_obj.main import Global
from core.world.base.map_save import MapSave
from core.world.base.visual.world import VisualWorld

from game_client.game_match.stages.common.chat import ChatPart
from game_client.game_match.stages.setup_menu.settings.buttons import BUTTONS_DATA
from game_client.game_match.stages.setup_menu.settings.maps_stuff import MapFuncUI
from game_client.game_match.stages.setup_menu.settings.maps_stuff import MapRect, MapsButtonsContainer

from visual.UI.base.menu import Menu
from visual.UI.base.container import Container
from visual.UI.popup_controller import PopUpsController
from visual.UI.base.mixins import DrawElementBorderMixin


class SetupMenu(Menu, PopUpsController, ChatPart, DrawElementBorderMixin):
    def __init__(self, setup_stage):
        super(SetupMenu, self).__init__(BUTTONS_DATA)
        PopUpsController.__init__(self)
        ChatPart.__init__(self)
        self.setup_stage = setup_stage
        self.w: VisualWorld = VisualWorld(MapRect.rect)
        self.maps_mngr = setup_stage.maps_mngr

        self.current_save: int = 0
        self.maps_cont = Container('container', True,
                                   parent=self,
                                   x_k=MapsButtonsContainer.X, y_k=MapsButtonsContainer.Y,
                                   h_size_k=MapsButtonsContainer.H_size,
                                   v_size_k=MapsButtonsContainer.V_size)

    def update(self):
        Global.display.fill((0, 0, 0))
        self.update_and_draw_map()
        for b in self.buttons:
            b.draw()
            if b.active and b.collide_point(Global.mouse.pos):
                self.draw_border_around_element(b)
                if Global.mouse.l_up:
                    b.do_action()

        self.upd_draw_map_container()
        self.update_chat()

    def load_save(self, save: MapSave):
        self.w.build_map_from_save(save)
        self.w.adapt_scale_to_win_size()

    def update_and_draw_map(self):
        self.w.draw()
        draw_rect(Global.display, (255, 255, 255), self.w.window_rect, 3)

    def fill_container(self):
        # self.maps_mngr.load_maps()
        # self.maps_cont.clear()
        for i, map_save in enumerate(self.maps_mngr.maps):
            self.maps_cont.add_element(MapFuncUI(uid=map_save.name, map_save=map_save,
                                                 parent=self.maps_cont, menu=self, index=i))

        self.maps_cont.build()

    def update_chosen_map(self, index: int, force=False):
        if self.current_save != index or force:
            self.current_save = index
            for i, save_c in enumerate(self.maps_cont.elements):
                if i == index:
                    self.load_save(save_c.save)
                    save_c.choose()
                else:
                    save_c.unchoose()
            self.maps_cont.render()

    def upd_draw_map_container(self):
        self.maps_cont.draw()
        if self.maps_cont.collide_point(Global.mouse.pos):
            if Global.mouse.scroll:
                self.maps_cont.change_dx(Global.mouse.scroll)

            mouse_pos = Global.mouse.pos
            for el in self.maps_cont.elements:
                if el.collide_point(mouse_pos):
                    if el.chosen_btn.collide_point(mouse_pos) and el.chosen_btn.active:
                        self.draw_border_around_element(el.chosen_btn)
                        if Global.mouse.l_up:
                            el.chosen_btn.do_action()
                            el: MapFuncUI
                    # elif el.delete_btn.collide_point(mouse_pos) and el.delete_btn.active:
                    #     self.draw_border_around_element(el.delete_btn)
                    #     if Global.mouse.l_up:
                    #         el.delete_btn.do_action()

                    self.draw_border_around_element(el)
