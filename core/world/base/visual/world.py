from typing import List
from pygame import draw, Surface, transform
from global_obj import Global
from core.world.base.logic.tile import LogicTile
from core.world.base.visual.tile import VisualTile
from core.world.base.logic.world import LogicWorld
from core.world.base.hex_utils import get_hex_math, HexMathAbs
from core.world.base.constants import TileDataAbs, IMPASSABLE_VALUE, TileTypes
from core.world.base.visual.tiles_textures import TilesTextures
from settings.tile_settings import TileSettings
from visual.UI.utils import get_surface


class VisualWorld(LogicWorld):

    def __init__(self, x, y, tile_size: int = TileSettings.visual_tile_r):
        super(VisualWorld, self).__init__(tile_class=VisualTile)
        self.textures = TilesTextures()
        self.x, self.y = x, y
        self.big_surface: Surface = None
        self.small_surface: Surface = None
        self.surface: Surface = None

        self.hex_math: HexMathAbs = None
        self.reference_hex: VisualTile = None
        self.tile_size: int = tile_size

        self.scale = 1

    def scale_surface(self):
        w, h = self.big_surface.get_size()
        self.surface = transform.smoothscale(self.big_surface, (int(w * self.scale), int(h * self.scale)))

    def build_map(self, flat, odd, data: List[List[TileDataAbs]]):
        self.hex_math = get_hex_math(flat, odd)
        super().build_map(flat, odd, data)
        self.big_surface = get_surface(*self.hex_math.get_map_size(self.x_size, self.y_size, self.tile_size))
        self.reference_hex = VisualTile((None, None), self.hex_math.get_dots_by_xy(0, 0, self.tile_size), '')
        self.render()

    def get_normalized_mouse(self):
        m_pos = self.hex_math.normalize_coordinates(Global.mouse.x - self.x,
                                                    Global.mouse.y - self.y,
                                                    self.tile_size)
        return m_pos[0] + self.x, m_pos[1] + self.y

    def render(self):
        self.big_surface.fill((10, 10, 10))
        for tile in self.tiles:
            self.render_tile(self.big_surface, tile)
        self.surface = self.big_surface.copy()

    def render_tile_by_xy(self, xy: tuple[int, int]):
        self.render_tile(self.surface, self.xy_to_tile[xy])

    def render_tile(self, surface, tile: VisualTile):
        pos = self.hex_math.get_lt_by_id(tile.id_x, tile.id_y, self.tile_size)
        draw.polygon(surface, tile.tile_data.color, tile.dots)
        draw.lines(surface, (50, 50, 50), True, points=tile.dots)

        # self.textures.get_texture()

    def get_tile_from_data(self, x, y, tile_data: TileDataAbs, **extra_data) -> VisualTile | LogicTile:
        dots = self.hex_math.get_dots_by_xy(x, y, self.tile_size)

        return super().get_tile_from_data(x=x, y=y, tile_data=tile_data, dots=dots)

    @staticmethod
    def draw_tile_border(surface, dots, color=(75, 75, 75), width=1):
        draw.lines(surface, color, True, dots, width)

    def draw(self):
        Global.display.blit(self.surface, (self.x, self.y))

    def save(self):
        pass


if __name__ == '__main__':
    from launch import GameRunner

    from visual.hex_stuff import get_colored_hex, draw_hex_border, rotate_hex
    import random


    class B:
        def __init__(self):
            self.w = VisualWorld(110, 0)
            self.HA = 0
            self.map_data = [[random.choice(tuple(TileTypes.types_dict.values())) for x in range(50)] for y in
                             range(25)]
            self.w.build_map(True, True, self.map_data)

        def game_loop(self):
            Global.display.fill((0, 0, 0))
            self.w.draw()
            # m_pos = self.w.get_normalized_mouse()
            draw.circle(Global.display, (255, 0, 0), self.w.get_normalized_mouse(), 3)
            pos = self.w.hex_math.get_indexes_from_coordinates(Global.mouse.x - self.w.x, Global.mouse.y - self.w.y,
                                                               self.w.tile_size)
            if pos in self.w.xy_to_tile:
                dots = self.w.hex_math.get_dots_by_xy(*pos, self.w.tile_size, self.w.x, self.w.y)
                self.w.draw_tile_border(Global.display, dots, color=(255, 255, 255))

            # x, y = self.w.get_normalized_mouse()
            # H = self.get_hexs()
            # Global.display.blit(H, (x - H.get_width() // 2, y - H.get_height() // 2))
            # if Global.mouse.l_up:
            #     self.HA += 1
            if Global.mouse.scroll:
                self.w.scale = self.w.scale + Global.mouse.scroll * Global.clock.d_time * 2
                # print(Global.mouse.scroll, self.w.scale)
                self.w.scale_surface()

        def get_hexs(self):
            H = get_colored_hex((100, 255, 100))
            draw_hex_border(H, (255, 255, 255))
            return rotate_hex(H, self.HA)


    GameRunner(B()).run()
