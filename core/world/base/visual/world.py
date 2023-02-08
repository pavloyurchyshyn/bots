if __name__ == '__main__':
    pass
from pygame.rect import Rect
from typing import List, Type
from _thread import start_new_thread
from pygame import draw, Surface, transform
from global_obj.main import Global
from visual.UI.utils import get_surface
from settings.tile_settings import TileSettings
from core.world.base.logic.tile import LogicTile
from core.world.base.visual.tile import VisualTile
from core.world.base.logic.world import LogicWorld
from core.world.base.logic.tiles_data import EmptyTile
from core.world.base.logic.tiles_data import TileDataAbs
from core.world.base.hex_utils import get_hex_math, HexMathAbs

from pygame.draw import circle as draw_circle


class VisualWorld(LogicWorld):

    def __init__(self, window_rect, tile_r: int = TileSettings.visual_tile_r, parent_surface=Global.display):
        super(VisualWorld, self).__init__(tile_class=VisualTile)
        self.parent_surface = parent_surface

        self.window_rect = Rect(window_rect)
        self.x, self.y, self.win_x_size, self.win_y_size = window_rect

        self.dx, self.dy = 0, 0

        self.big_surface: Surface = None
        self.small_surface: Surface = None
        self.surface: Surface = None

        self.hex_math: HexMathAbs = None
        self.reference_hex: VisualTile = None
        self.tile_r: int = tile_r
        self.tile_xy_size = (1, 1)  # self.hex_math.get_hex_size(self.tile_r)

        self.scale = 1

    def adapt_scale_to_win_size(self):
        h_size, v_size = self.hex_math.get_map_size(self.x_size, self.y_size, self.tile_r)
        h_k = self.window_rect[2] / h_size
        v_k = self.window_rect[3] / v_size
        self.scale = h_k if h_k < v_k else v_k
        self.reload_surface()

    @property
    def scaled_tile_size(self):
        return self.tile_r * self.scale

    def threaded_reload_surface(self, *add_funcs):
        start_new_thread(self.reload_surface, ())
        for func in add_funcs:
            func()

    def reload_surface(self):
        w, h = self.big_surface.get_size()
        self.surface = transform.smoothscale(self.big_surface, (int(w * self.scale), int(h * self.scale)))

    def build_map(self, flat, odd, data: List[List[TileDataAbs]]):
        self.hex_math = get_hex_math(flat, odd)
        self.tile_xy_size = self.hex_math.get_hex_size(self.tile_r)
        self.clear()
        super().build_map(flat, odd, data)
        self.reference_hex = VisualTile((None, None),
                                        center=(-100, -100),
                                        dots=self.hex_math.get_dots_by_xy(0, 0, self.tile_r),
                                        texture_size=self.hex_math.get_hex_size(self.tile_r))
        self.render()

    def create_big_surface(self):
        return get_surface(*self.hex_math.get_map_size(self.x_size, self.y_size, self.tile_r))

    def build_map_from_save(self, save):
        self.build_map(save.flat, save.odd, save.get_tiles_data())

    def init_hex_math(self, flat=True, odd=True):
        self.hex_math = get_hex_math(flat, odd)

    def get_normalized_mouse_pos(self) -> tuple[int, int]:
        m_pos = self.hex_math.normalize_coordinates(Global.mouse.x - self.x - self.dx,
                                                    Global.mouse.y - self.y - self.dy,
                                                    self.scaled_tile_size)
        return m_pos[0] + self.x + self.dx, m_pos[1] + self.y + self.dy

    def get_mouse_to_xy(self):
        return self.hex_math.get_indexes_from_coordinates(
            (Global.mouse.x - self.x - self.dx) / self.scale,
            (Global.mouse.y - self.y - self.dy) / self.scale,
            self.tile_r)

    def get_tile_under_mouse(self) -> LogicTile:
        return self.xy_to_tile.get(self.get_mouse_to_xy())

    def render(self):
        self.big_surface = self.create_big_surface()
        self.big_surface.fill((0, 0, 0))
        for tile in self.tiles:
            self.render_tile(self.big_surface, tile)
        self.surface = self.big_surface.copy()

    def render_tile_by_xy(self, xy: tuple[int, int]):
        self.render_tile(self.big_surface, self.xy_to_tile[xy])

    def rerender_tile(self, xy: tuple[int, int]):
        self.render_tile(self.big_surface, self.xy_to_tile[xy])
        self.reload_surface()

    def render_tile(self, surface, tile: VisualTile):
        # pos = self.hex_math.get_lt_by_id(tile.id_x, tile.id_y, self.tile_size)
        if tile.tile_data.name == EmptyTile.name:
            # draw.polygon(surface, (0, 0, 0), tile.dots)
            # draw.lines(surface, (0, 0, 0), True, points=tile.dots)
            draw_circle(surface, (30, 30, 30), tile.center, 3)
            if tile.at_edge:
                draw.lines(surface, (200, 200, 255), True, points=tile.dots, width=3)
            return

        # draw.polygon(surface, tile.tile_data.color, tile.dots)
        # draw.lines(surface, (50, 50, 50), True, points=tile.dots)
        surface.blit(Global.textures.get_scaled_tile_texture(tile.name, tile.img, tile.texture_size), tile.texture_pos)
        draw_circle(surface, (255, 0, 0), tile.center, 3)
        # draw.rect(surface, (255, 255, 255), (tile.texture_pos, tile.texture.get_size()), 1)
        if tile.at_edge:
            draw.lines(surface, (200, 200, 255), True, points=tile.dots, width=3)

        # font = get_custom_font(int(9 * self.scale))
        # text = font.render(f'{tile.id_x, tile.id_y}', True, (255, 255, 255))
        # pos = self.hex_math.get_center_by_xy_id(tile.id_x, tile.id_y, self.tile_size)
        # surface.blit(text, (pos[0] - text.get_width() // 2, pos[1] - text.get_height() // 2))
        # self.textures.get_texture()

    def get_tile_from_data(self, x, y, tile_data: Type[TileDataAbs], **extra_data) -> VisualTile | LogicTile:
        dots = self.hex_math.get_dots_by_xy(x, y, self.tile_r)
        return super().get_tile_from_data(x=x, y=y,
                                          tile_data=tile_data,
                                          dots=dots,
                                          texture_size=self.tile_xy_size,
                                          center=self.hex_math.get_center_by_xy_id(x, y, self.tile_r),
                                          **extra_data)

    def draw_border_for_xy(self, xy, color=(255, 255, 255)):
        self.draw_tile_border(Global.display, self.get_dots_due_to_map_pos(*xy), color=color)

    def draw_border_under_mouse(self, color=(255, 255, 255)):
        if self.window_rect.collidepoint(Global.mouse.pos):
            pos = self.get_mouse_to_xy()
            if pos in self.xy_to_tile:
                self.draw_border_for_xy(pos, color)

    @staticmethod
    def draw_tile_border(surface, dots, color=(75, 75, 75), width=1):
        draw.lines(surface, color, True, dots, width)

    def get_dots_due_to_map_pos(self, x, y):
        return self.hex_math.get_dots_by_xy(x, y,
                                            self.scaled_tile_size,
                                            self.x + self.dx,
                                            self.y + self.dy)

    def draw(self):
        if self.surface:
            self.parent_surface.blit(self.surface,
                                     (self.x, self.y),
                                     (0 - self.dx, 0 - self.dy, self.win_x_size, self.win_y_size))

    def get_real_center_of_tile(self, xy: tuple) -> tuple:
        x, y = self.hex_math.get_center_by_xy_id(*xy, self.tile_r)
        return int(x * self.scale) + self.dx + self.x, int(y * self.scale) + self.y + self.dy

    def get_real_lt_of_tile(self, xy: tuple) -> tuple:
        x, y = self.hex_math.get_lt_by_id(*xy, self.tile_r)
        return int(x * self.scale) + self.dx + self.x, int(y * self.scale) + self.y + self.dy
