from global_obj.main import Global
from pygame.draw import rect as draw_rect
from visual.UI.utils import get_surface
from visual.UI.timer import Timer
from visual.UI.base.menu import Menu
from visual.UI.base.button import Button
from visual.UI.base.window import Window
from game_client.game_match.stages.match_menu.settings.windows_sizes import ReadyWindow


class ReadyW(Window):
    parent: Menu

    def __init__(self, menu):
        surface = get_surface(ReadyWindow.h_size, ReadyWindow.v_size, color=(50, 50, 50))
        super().__init__(uid='ready_win', parent=menu,
                         x=ReadyWindow.x, y=ReadyWindow.y,
                         surface=surface,
                         h_size=ReadyWindow.h_size, v_size=ReadyWindow.v_size)
        self.ready_btn: Button = Button('ready_btn', 'Ready',
                                        x_k=ReadyWindow.RBtn_x_k,
                                        y_k=ReadyWindow.RBtn_y_k,
                                        h_size_k=ReadyWindow.RBtn_h_size,
                                        v_size_k=ReadyWindow.RBtn_v_size,
                                        ).build()
        self.timer = Timer('timer', x_k=ReadyWindow.Timer_x_k, y_k=ReadyWindow.Timer_y_k,
                           h_size_k=ReadyWindow.Timer_h_size, v_size_k=ReadyWindow.Timer_v_size)
        Global.round_clock.set_time(-60)

    def update(self):
        Global.display.blit(self.surface, self.real_position)
        self.update_ready_btn()

        self.timer.update()
        self.timer.draw()

        draw_rect(Global.display, (255, 255, 255), ReadyWindow.rect, 1)

    def update_ready_btn(self):
        self.ready_btn.draw()
        if self.ready_btn.collide_point(Global.mouse.pos):
            self.parent.draw_border_around_element(self.ready_btn)
            if Global.mouse.l_up:
                self.ready_btn.do_action()
