from global_obj.main import Global
from pygame.draw import rect as draw_rect
from visual.UI.utils import get_surface
from visual.UI.timer import Timer
from visual.UI.base.menu import Menu
from visual.UI.base.text import Text
from visual.UI.base.button import Button
from visual.UI.base.window import Window
from game_client.game_match.stages.match_menu.settings.windows_sizes import ReadyWindow
from server_stuff.constants.requests import GameStgConst as GSC


class ReadyW(Window):
    parent: Menu

    def __init__(self, menu):
        surface = get_surface(ReadyWindow.h_size, ReadyWindow.v_size, color=(50, 50, 50))
        super().__init__(uid='ready_win', parent=menu,
                         x=ReadyWindow.x, y=ReadyWindow.y,
                         surface=surface,
                         h_size=ReadyWindow.h_size, v_size=ReadyWindow.v_size)
        self.ready_players: Text = Text('ready_players_text', '0/0',
                                        raw_text=True,
                                        x_k=ReadyWindow.ReadyPlayers_x,
                                        y_k=ReadyWindow.ReadyPlayers_y,
                                        h_size_k=ReadyWindow.ReadyPlayers_h_size,
                                        v_size_k=ReadyWindow.ReadyPlayers_v_size,
                                        )
        self.ready_btn: Button = Button('ready_btn', 'Ready',
                                        x_k=ReadyWindow.RBtn_x_k,
                                        y_k=ReadyWindow.RBtn_y_k,
                                        h_size_k=ReadyWindow.RBtn_h_size,
                                        v_size_k=ReadyWindow.RBtn_v_size,
                                        on_click_action=self.ready_click_action,
                                        ).build()

        self.timer = Timer('timer', x_k=ReadyWindow.Timer_x_k, y_k=ReadyWindow.Timer_y_k,
                           h_size_k=ReadyWindow.Timer_h_size, v_size_k=ReadyWindow.Timer_v_size)

        Global.round_clock.set_time(-60)

    def change_button_color_to_ready(self):
        self.ready_btn.text.change_color((0, 255, 0) if self.parent.player.ready else (255, 255, 255))
        self.ready_btn.render()

    def ready_click_action(self, b: Button):
        Global.logger.info(f'Request ready to {not self.parent.player.ready}')
        Global.connection.send_json({GSC.Player.ReadyStatus: not self.parent.player.ready})

    def update(self):
        Global.display.blit(self.surface, self.real_position)
        self.update_ready_btn()
        self.timer.update()
        self.timer.draw()

        self.ready_players.draw()

        draw_rect(Global.display, (255, 255, 255), ReadyWindow.rect, 1)

    def update_ready_btn(self):
        self.ready_btn.draw()
        if self.ready_btn.collide_point(Global.mouse.pos):
            self.parent.draw_border_around_element(self.ready_btn)
            if Global.mouse.l_up:
                self.ready_btn.do_action()

    def set_ready_players_text(self, txt: str):
        self.ready_players.change_text(txt)
