from typing import Callable, Dict

from pygame import Surface

from global_obj.main import Global
from visual.UI.base.abs import ShapeAbs
from visual.UI.base.text import Text
from visual.UI.base.button import Button
from visual.UI.base.container import Container
from visual.styles import get_red_btn_style
from game_client.game_match.stages.setup_menu.settings.connected_players_and_slots import *
from visual.UI.base.element import BaseUI, GetSurfaceMixin, DrawBorderMixin, BuildRectShapeMixin
from settings.localization.menus.UI import UILocal

from server_stuff.constants.requests import SetupStageReq


class PlayerSlot(BaseUI, ShapeAbs, BuildRectShapeMixin, GetSurfaceMixin, DrawBorderMixin):
    parent: Container

    def __init__(self,
                 uid: str,
                 nickname: str,
                 token: str,
                 slot: int,
                 parent: Container,
                 x_k: float = 0.01,
                 y_k: float = 0,
                 h_size_k: float = PlayerBlockCnst.H_SIZE,
                 v_size_k: float = PlayerBlockCnst.V_SIZE,
                 **kwargs):
        super(PlayerSlot, self).__init__(uid,
                                         x_k=x_k,
                                         y_k=y_k,
                                         h_size_k=h_size_k,
                                         v_size_k=v_size_k,
                                         parent=parent,
                                         **kwargs)
        ShapeAbs.__init__(self, **kwargs)
        self.nickname: str = nickname
        self.token: str = token
        self.slot: int = int(slot)
        self.slot_text: Text = Text('',
                                    x_k=0.02,
                                    h_size_k=0.5,
                                    text=f'{self.slot + 1}. {self.nickname}',
                                    parent=self,
                                    from_left=True,
                                    )
        show_button = Global.network_data.is_admin or self.token == Global.network_data.token

        self.deselect_btn: Button = Button('',
                                           x_k=0.945,
                                           h_size_k=0.05,
                                           v_size_k=0.92,
                                           text='X',
                                           parent=self,
                                           style=get_red_btn_style(),
                                           active=show_button and self.token,
                                           on_click_action=self.deselect_slot,
                                           # postpone_build=True,
                                           )

        self.pick_slot_btn: Button = Button('',
                                            x_k=0.84,
                                            h_size_k=0.1,
                                            v_size_k=0.92,
                                            text=UILocal.SetupStageMenu.pick,
                                            parent=self,
                                            active=self.token is None,
                                            visible=self.token is None,
                                            on_click_action=self.pick_slot,
                                            # postpone_build=True,
                                            )
        self.set_bot_btn: Button = Button('',
                                          x_k=0.735,
                                          h_size_k=0.1,
                                          v_size_k=0.92,
                                          text=UILocal.SetupStageMenu.bot,
                                          parent=self,
                                          active=self.token is None and Global.network_data.is_admin,
                                          visible=self.token is None and Global.network_data.is_admin,
                                          on_click_action=self.set_bot,
                                          # postpone_build=True,
                                          )

        self.buttons = self.deselect_btn, self.pick_slot_btn, self.set_bot_btn
        self.build()

    def set_bot(self, b: Button):
        if self.token is None and Global.network_data.is_admin:
            Global.connection.send_json({SetupStageReq.SetBot: self.slot})

    def pick_slot(self, b: Button):
        if self.token is None:
            Global.connection.send_json({SetupStageReq.SelectSlot: self.slot})

    def deselect_slot(self, b: Button):
        if Global.network_data.is_admin or self.token == Global.network_data.token:
            Global.connection.send_json({SetupStageReq.DeselectSlot: self.slot})

    def draw(self):
        self.parent_surface.blit(self.surface, self.position)

    def get_x(self) -> int:
        return self.default_get_x()

    def get_y(self) -> int:
        return self.default_get_y()

    def build(self, **kwargs):
        self.init_shape()
        # self.deselect_btn.build()
        # self.pick_slot_btn.build()
        # self.set_bot_btn.build()
        self.render()
        return self

    def render(self, **kwargs):
        self.fill_surface()
        self.slot_text.draw()
        self.deselect_btn.draw()
        self.pick_slot_btn.draw()
        self.set_bot_btn.draw()
        self.draw_border()

    def move(self, xy):
        self.x, self.y = xy
        self.init_shape()
        self.deselect_btn.init_shape()
        self.pick_slot_btn.init_shape()
        self.set_bot_btn.init_shape()

    def get_surface(self, **kwargs) -> Surface:
        return self.get_rect_surface(self.h_size, self.v_size,
                                     transparent=self.style.surface_transparent,
                                     flags=self.style.surface_flags)

    def fill_surface(self, surface=None, color=(100, 100, 100)) -> None:
        self.fill_surface_due_to_border_attrs(surface, color)

    def init_shape(self) -> None:
        self.init_rect_shape()


class PlayersSlots:
    def __init__(self):
        self.players_slots: Container = Container('players_slots',
                                                  draw_elements=True,
                                                  parent=self,
                                                  x_k=PlayersSlotsCnst.X,
                                                  y_k=PlayersSlotsCnst.Y,
                                                  h_size_k=PlayersSlotsCnst.H_SIZE,
                                                  v_size_k=PlayersSlotsCnst.V_SIZE,
                                                  )

        self.players_slots.build()

    def fill_players_slots(self, conn_players: dict):
        self.players_slots.clear()
        for slot, (token, nickname) in conn_players.items():
            self.players_slots.add_element(PlayerSlot(uid=f"{slot}_slot_uid",
                                                      nickname=nickname,
                                                      token=token,
                                                      slot=slot,
                                                      parent=self.players_slots,
                                                      ))
        self.players_slots.build()

    def update_draw_players_slots_container(self):
        self.players_slots.draw()
        if self.players_slots.collide_point(Global.mouse.pos):
            if Global.mouse.scroll:
                self.players_slots.change_dx(Global.mouse.scroll)

            mouse_pos = Global.mouse.pos
            for el in self.players_slots.elements:
                if el.collide_point(mouse_pos):
                    el: PlayerSlot
                    for btn in el.buttons:
                        if btn.collide_point(mouse_pos) and btn.active:
                            self.draw_border_around_element(btn)
                            if Global.mouse.l_up:
                                btn.do_action()
                            break

                    self.draw_border_around_element(el)
