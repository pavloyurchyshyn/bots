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

from server_stuff.constants.requests import CommonReqConst


class ConnectedPlayerBlock(BaseUI, ShapeAbs, BuildRectShapeMixin, GetSurfaceMixin, DrawBorderMixin):
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
        super(ConnectedPlayerBlock, self).__init__(uid,
                                                   x_k=x_k,
                                                   y_k=y_k,
                                                   h_size_k=h_size_k,
                                                   v_size_k=v_size_k,
                                                   parent=parent,
                                                   **kwargs)
        ShapeAbs.__init__(self, **kwargs)
        self.nickname: str = nickname
        self.token: str = token
        self.slot: int = slot
        self.nickname_text: Text = Text('',
                                        x_k=0.02,
                                        text=self.nickname,
                                        parent=self,
                                        from_left=True,
                                        )
        show_button = Global.network_data.is_admin and self.token != Global.network_data.token

        self.kick_btn: Button = Button('',
                                       x_k=0.945,
                                       h_size_k=0.05,
                                       v_size_k=0.92,
                                       text='X',
                                       parent=self,
                                       style=get_red_btn_style(),
                                       active=show_button,
                                       visible=show_button,
                                       on_click_action=self.kick_player,
                                       )
        self.build()

    def kick_player(self, b: Button):
        if Global.network_data.is_admin and self.token != Global.network_data.token:
            Global.connection.send_json({CommonReqConst.KickPlayer: self.token})

    def draw(self):
        self.parent_surface.blit(self.surface, self.position)

    def get_x(self) -> int:
        return self.default_get_x()

    def get_y(self) -> int:
        return self.default_get_y()

    def build(self, **kwargs):
        self.render()
        self.init_shape()
        self.kick_btn.build()
        return self

    def render(self, **kwargs):
        self.fill_surface()
        self.nickname_text.draw()
        self.kick_btn.draw()
        self.draw_border()

    def move(self, xy):
        self.x, self.y = xy
        self.init_shape()
        self.kick_btn.init_shape()

    def get_surface(self, **kwargs) -> Surface:
        return self.get_rect_surface(self.h_size, self.v_size,
                                     transparent=self.style.surface_transparent,
                                     flags=self.style.surface_flags)

    def fill_surface(self, surface=None, color=(100, 100, 100)) -> None:
        self.fill_surface_due_to_border_attrs(surface, color)

    def init_shape(self) -> None:
        self.init_rect_shape()


class ConnectedPlayers:
    def __init__(self):
        self.connected_players: Container = Container('connected_players',
                                                      draw_elements=True,
                                                      parent=self,
                                                      x_k=ConnectedPlayerCnst.X,
                                                      y_k=ConnectedPlayerCnst.Y,
                                                      h_size_k=ConnectedPlayerCnst.H_SIZE,
                                                      v_size_k=ConnectedPlayerCnst.V_SIZE,
                                                      )

        self.connected_players.build()

    def fill_connected(self, conn_players: dict):
        self.connected_players.clear()
        for token, (slot, nickname) in conn_players.items():
            self.connected_players.add_element(ConnectedPlayerBlock(uid=f"{nickname}_uid",
                                                                    nickname=nickname,
                                                                    token=token,
                                                                    slot=slot,
                                                                    parent=self.connected_players,
                                                                    ))
        self.connected_players.build()

    def update_draw_connected_players_container(self):
        self.connected_players.draw()
        if self.connected_players.collide_point(Global.mouse.pos):
            if Global.mouse.scroll:
                self.connected_players.change_dy(Global.mouse.scroll)

            mouse_pos = Global.mouse.pos
            for el in self.connected_players.elements:
                if el.collide_point(mouse_pos):
                    if el.kick_btn.collide_point(mouse_pos) and el.kick_btn.active:
                        self.draw_border_around_element(el.kick_btn)
                        if Global.mouse.l_up:
                            el.kick_btn.do_action()
                            el: ConnectedPlayerBlock
                    # elif el.delete_btn.collide_point(mouse_pos) and el.delete_btn.active:
                    #     self.draw_border_around_element(el.delete_btn)
                    #     if Global.mouse.l_up:
                    #         el.delete_btn.do_action()

                    self.draw_border_around_element(el)
