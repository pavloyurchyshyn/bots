from pygame.draw import rect as draw_rect

from global_obj.main import Global
from core.world.base.map_save import MapSave
from core.world.base.visual.world import VisualWorld

from game_client.game_match.stages.common.chat import ChatPart
from game_client.game_match.stages.setup_menu.settings.buttons import BUTTONS_DATA
from game_client.game_match.stages.setup_menu.settings.maps_stuff import MapChooseUI
from game_client.game_match.stages.setup_menu.settings.maps_stuff import MapRect, MapsButtonsContainer
from game_client.game_match.stages.setup_menu.components.players_slots import PlayersSlots
from game_client.game_match.stages.setup_menu.components.connected_players import ConnectedPlayers
from game_client.game_match.stages.setup_menu.settings.connected_players_and_slots import *

from visual.UI.base.menu import Menu
from visual.UI.base.button import Button
from visual.UI.base.input import InputBase
from visual.UI.base.container import Container
from visual.UI.popup_controller import PopUpsController
from visual.UI.base.mixins import DrawElementBorderMixin

from server_stuff.constants.requests import SetupStageReq


class SetupMenu(Menu,
                PopUpsController, ChatPart,
                ConnectedPlayers,
                PlayersSlots,
                DrawElementBorderMixin):
    start: Button

    def __init__(self, setup_stage):
        super(SetupMenu, self).__init__(BUTTONS_DATA)
        PopUpsController.__init__(self)
        ChatPart.__init__(self)
        ConnectedPlayers.__init__(self)
        PlayersSlots.__init__(self)
        self.setup_stage = setup_stage
        self.w: VisualWorld = VisualWorld(MapRect.rect)
        self.maps_mngr = setup_stage.maps_mngr

        self.current_save: int = 0
        self.maps_container: Container = Container('maps_container',
                                                   True,
                                                   parent=self,
                                                   x_k=MapsButtonsContainer.X, y_k=MapsButtonsContainer.Y,
                                                   h_size_k=MapsButtonsContainer.H_size,
                                                   v_size_k=MapsButtonsContainer.V_size)
        self.start.set_active(Global.network_data.is_admin)
        self.start.set_visible(Global.network_data.is_admin)

        self.nickname_input: InputBase = InputBase('nickname_input',
                                                   text=Global.network_data.nickname,
                                                   default_text='Enter nickname',
                                                   parent=self,
                                                   x_k=NicknameInput.X,
                                                   y_k=NicknameInput.Y,
                                                   h_size_k=NicknameInput.H_SIZE,
                                                   v_size_k=NicknameInput.V_SIZE,
                                                   on_enter_action=self.nickname_function,
                                                   )
        self.submit_nickname: Button = Button('submit_nickname',
                                              text='Upd',
                                              parent=self,
                                              on_click_action=self.nickname_function,
                                              active=False,
                                              x_k=NicknameInputBtn.X,
                                              y_k=NicknameInputBtn.Y,
                                              h_size_k=NicknameInputBtn.H_SIZE,
                                              v_size_k=NicknameInputBtn.V_SIZE,
                                              )

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
        self.update_draw_connected_players_container()
        self.update_draw_players_slots_container()
        self.update_and_draw_nickname_inp()

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
            self.maps_container.add_element(MapChooseUI(uid=map_save.name, map_save=map_save,
                                                        parent=self.maps_container, menu=self, index=i))

        self.maps_container.build()

    def update_chosen_map(self, index: int, force=False):
        if self.current_save != index or force:
            self.current_save = index
            for i, save_c in enumerate(self.maps_container.elements):
                if i == index:
                    self.load_save(save_c.save)
                    save_c.choose()
                else:
                    save_c.unchoose()
            self.maps_container.render()

    def upd_draw_map_container(self):
        self.maps_container.draw()
        if self.maps_container.collide_point(Global.mouse.pos):
            if Global.mouse.scroll:
                self.maps_container.change_dx(Global.mouse.scroll)

            mouse_pos = Global.mouse.pos
            for el in self.maps_container.elements:
                if el.collide_point(mouse_pos):
                    if el.chosen_btn.collide_point(mouse_pos) and el.chosen_btn.active:
                        self.draw_border_around_element(el.chosen_btn)
                        if Global.mouse.l_up:
                            el.chosen_btn.do_action()
                            el: MapChooseUI
                    # elif el.delete_btn.collide_point(mouse_pos) and el.delete_btn.active:
                    #     self.draw_border_around_element(el.delete_btn)
                    #     if Global.mouse.l_up:
                    #         el.delete_btn.do_action()

                    self.draw_border_around_element(el)

    def update_and_draw_nickname_inp(self):
        self.nickname_input.draw()
        if self.nickname_input.collide_point(Global.mouse.pos):
            self.draw_border_around_element(self.nickname_input)
            if Global.mouse.l_up:
                self.nickname_input.focus()
        self.nickname_input.update()
        self.submit_nickname.set_active(Global.network_data.nickname != self.nickname_input.text.str_text)

        if self.submit_nickname.collide_point(Global.mouse.pos):
            self.draw_border_around_element(self.submit_nickname)
            if Global.mouse.l_up and self.submit_nickname.active:
                self.submit_nickname.do_action()
        self.submit_nickname.draw()

    def nickname_function(self, i: InputBase = None):
        name = self.nickname_input.text.str_text
        if name:
            Global.network_data.nickname = name
            Global.connection.send_json({SetupStageReq.Player.NewNickname: name})
