from pygame.draw import rect as draw_rect

from global_obj.main import Global

from core.world.base.visual.world import VisualWorld
from settings.screen.size import scaled_w, scaled_h
from game_client.game_match.stages.match_menu.settings.windows_sizes import MapRect


class WorldC:
    def __init__(self):
        self.w: VisualWorld = VisualWorld(MapRect.rect, tile_r=scaled_w(0.03))

    def update_and_draw_map(self):
        self.check_for_drag()
        self.check_for_scale()

        self.w.draw()
        draw_rect(Global.display, (255, 255, 255), self.w.window_rect, 1)
        self.w.draw_border_under_mouse()

    def check_for_drag(self):
        if Global.mouse.m_hold:
            self.w.dx += Global.mouse.rel_x
            self.w.dy += Global.mouse.rel_y
            self.define_map_position()

    def check_for_scale(self):
        if scroll := Global.mouse.scroll:
            if self.w.window_rect.collidepoint(*Global.mouse.pos):
                map_bigger = True
                if self.w.surface.get_width() * 1.02 < MapRect.h_size \
                        and self.w.surface.get_height() * 1.02 < MapRect.v_size:
                    map_bigger = False

                if scroll > 0 or (scroll < 0 and map_bigger):
                    self.w.scale = self.w.scale + scroll * Global.clock.d_time
                    # TODO add minimum scale parameter due to rect size
                    self.w.reload_surface()
                    self.define_map_position()
                    # self.w.threaded_reload_surface()

    def define_map_position(self):
        if MapRect.h_size > self.w.surface.get_width():
            self.w.dx = (MapRect.h_size - self.w.surface.get_width()) // 2
        elif self.w.dx > 0:
            self.w.dx = 0
        elif self.w.surface.get_width() + self.w.dx < MapRect.h_size:
            self.w.dx = MapRect.h_size - self.w.surface.get_width()

        if MapRect.v_size > self.w.surface.get_height():
            self.w.dy = (MapRect.v_size - self.w.surface.get_height()) // 2
        elif self.w.dy > 0:
            self.w.dy = 0
        elif self.w.surface.get_height() + self.w.dy < MapRect.v_size:
            self.w.dy = MapRect.v_size - self.w.surface.get_height()
