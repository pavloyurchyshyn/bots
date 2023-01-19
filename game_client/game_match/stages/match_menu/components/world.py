from pygame.draw import rect as draw_rect

from global_obj.main import Global

from core.world.base.map_save import MapSave
from core.world.base.visual.world import VisualWorld
from settings.screen.size import scaled_w


class MapRect:
    from settings.screen.size import scaled_w, scaled_h

    H_size = scaled_w(0.8)
    V_size = scaled_h(0.7)
    X = 0
    Y = scaled_h(0.05)
    rect = (X, Y, H_size, V_size)


class WorldC:
    def __init__(self):
        self.w: VisualWorld = VisualWorld(MapRect.rect, tile_size=scaled_w(0.03))

    def update_and_draw_map(self):
        self.check_for_drag()
        self.check_for_scale()

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
                map_bigger = True
                if self.w.surface.get_width() * 1.02 < MapRect.H_size \
                        and self.w.surface.get_height() * 1.02 < MapRect.V_size:
                    map_bigger = False

                if scroll > 0 or (scroll < 0 and map_bigger):
                    self.w.scale = self.w.scale + scroll * Global.clock.d_time * 2
                    #self.w.reload_surface()
                    #self.define_map_position()
                    self.w.threaded_reload_surface(self.define_map_position)

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
