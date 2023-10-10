from pygame.rect import Rect
from typing import List, Type, Tuple, Optional, Dict
from _thread import start_new_thread
from pygame import draw, Surface, transform
from global_obj.main import Global
from visual.UI.utils import get_surface
from visual.UI.base.text import Text
from settings.tile_settings import TileSettings
from core.world.base.logic.tile import LogicTile
from core.world.base.visual.tile import VisualTile
from core.world.base.logic.world import LogicWorld
from core.world.base.logic.tiles_data import EmptyTile
from core.world.base.logic.tiles_data import TileDataAbs
from core.world.base.hex_utils import HexMath, Cube
from core.shape.hex import Hex
from settings.visual.graphic import GraphicConfig


class VisualWorld(LogicWorld):
    tiles: List[VisualTile]
    MAX_SCALE = 1

    def __init__(self, window_rect, tile_radius: int = TileSettings.visual_tile_radius, parent_surface=Global.display):
        super(VisualWorld, self).__init__(tile_class=VisualTile)
        self.parent_surface = parent_surface

        self.window_rect = Rect(window_rect)
        self.x, self.y, self.win_x_size, self.win_y_size = window_rect

        self.dx, self.dy = 0, 0

        self.big_surface: Surface = None
        self.surface: Surface = None
        self.surface_back_color = (50, 50, 50)

        self.tile_radius: int = tile_radius
        self.tile_size = self.hex_math.get_hex_size(self.tile_radius)
        self.cached_rays: Dict[Tuple, List[Tuple[int, int]]] = {}

        self.scale = 1

        self.missing_tile_texture: Surface = None
        self.render_missing_tile()

    def render_missing_tile(self):
        # TODO make some better image
        surface: Surface = get_surface(h_size=self.tile_size[0], v_size=self.tile_size[0], transparent=1)
        draw.polygon(surface, (200, 0, 0), Hex(0, self.tile_size[0] - self.tile_size[1], self.tile_radius).dots[1:])
        text = Text('', text='?', parent_surface=surface, font_size=GraphicConfig.FontSize * 2)
        text.draw()
        self.missing_tile_texture = surface

    def adapt_scale_to_win_size(self):
        h_size, v_size = self.hex_math.get_grid_size(self.x_size, self.y_size, self.tile_radius)
        h_k = self.window_rect.width / h_size
        v_k = self.window_rect.height / v_size
        self.scale = h_k if h_k < v_k else v_k
        self.reload_surface()

    @property
    def scaled_tile_radius(self) -> int:
        return self.tile_radius * self.scale

    def threaded_reload_surface(self, *add_funcs):
        start_new_thread(self.reload_surface, ())
        for func in add_funcs:
            func()

    def reload_surface(self):
        w, h = self.big_surface.get_size()
        self.surface = transform.smoothscale(self.big_surface, (int(w * self.scale), int(h * self.scale)))

    def build_map(self, data: List[List[TileDataAbs]]):
        self.clear()
        super().build_map(data)

        self.render()

    def create_big_surface(self) -> Surface:
        return get_surface(*self.hex_math.get_grid_size(self.x_size, self.y_size, self.tile_radius),
                           color=self.surface_back_color)

    def build_map_from_save(self, save):
        self.build_map(save.get_tiles_data())

    def get_mouse_to_xy(self):
        return self.hex_math.normalize_coordinates(
            (Global.mouse.x - self.x - self.dx) / self.scale,
            (Global.mouse.y - self.y - self.dy) / self.scale,
            self.tile_radius)

    def get_tile_under_mouse(self) -> VisualTile:
        return self.get_tile_by_xy(self.get_mouse_to_xy())

    def get_tile_by_xy(self, xy: Tuple[int, int]) -> Optional[VisualTile]:
        return super().get_tile_by_xy(xy)

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

    @staticmethod
    def get_scaled_texture_from_tile(tile: VisualTile):
        return Global.textures.get_scaled_tile_texture(tile_type=tile.name,
                                                       img=tile.img,
                                                       size=tile.texture_size, raise_error=True)

    def render_tile(self, surface, tile: VisualTile):
        if tile.name == EmptyTile.name:
            return

        try:
            surface.blit(self.get_scaled_texture_from_tile(tile=tile), tile.texture_pos)
        except FileNotFoundError:
            surface.blit(self.missing_tile_texture, tile.texture_pos)

        # draw_circle(surface, (255, 0, 0), tile.center, 3)
        # draw.rect(surface, (255, 255, 255), (tile.texture_pos, tile.texture.get_size()), 1)
        if tile.at_edge:
            draw.lines(surface, (200, 200, 255), True, points=tile.dots, width=3)

        # from visual.UI.base.font import get_custom_font
        # font = get_custom_font(int(self.big_surface.get_width() // 300))
        # text = font.render(f'{tile.xy_id}', True, (255, 255, 255))
        # pos = self.hex_math.xy_id_to_xy_coordinates(tile.x_id, tile.y_id, self.tile_radius)
        # surface.blit(text, (pos[0] - text.get_width() // 2, pos[1] - text.get_height() // 2 - 5))
        #
        # text = font.render(f'{tile.qrs}', True, (255, 255, 255))
        # pos = self.hex_math.xy_id_to_xy_coordinates(tile.x_id, tile.y_id, self.tile_radius)
        # surface.blit(text, (pos[0] - text.get_width() // 2, pos[1] - text.get_height() // 2 + 5))
        # self.textures.get_texture()

    def get_tile_from_data(self, x, y, tile_data: Type[TileDataAbs], **extra_data) -> VisualTile | LogicTile:
        return super().get_tile_from_data(x=x, y=y,
                                          tile_data=tile_data,
                                          radius=self.tile_radius,
                                          **extra_data)

    def draw_border_for_xy(self, xy, color=(255, 255, 255), width=1):
        self.draw_tile_border(Global.display, self.get_dots_due_to_map_pos(*xy), color=color, width=width)

    def draw_border_under_mouse(self, color=(255, 255, 255)):
        if self.window_rect.collidepoint(Global.mouse.pos):
            pos = self.get_mouse_to_xy()
            if pos in self.xy_to_tile:
                self.draw_border_for_xy(pos, color)

    @staticmethod
    def draw_tile_border(surface, dots, color=(75, 75, 75), width=1):
        draw.lines(surface, color, True, dots, width)

    def get_dots_due_to_map_pos(self, x, y):
        return self.hex_math.get_dots_by_xy_id(x, y,
                                               self.scaled_tile_radius,
                                               self.x + self.dx,
                                               self.y + self.dy,
                                               )

    def draw(self):
        if self.surface:
            self.parent_surface.blit(self.surface,
                                     (self.x, self.y),
                                     (0 - self.dx, 0 - self.dy, self.win_x_size, self.win_y_size))

    def get_real_center_of_tile(self, xy: tuple) -> tuple:
        x, y = self.hex_math.xy_id_to_xy_coordinates(*xy, self.tile_radius)
        return int(x * self.scale) + self.dx + self.x, int(y * self.scale) + self.y + self.dy

    def get_real_center_of_tile_qr(self, qr: tuple) -> tuple:
        x, y = self.hex_math.qr_to_xy_coords(*qr, self.tile_radius)
        return int(x * self.scale) + self.dx + self.x, int(y * self.scale) + self.y + self.dy

    def draw_ray_from_a_to_b_xy(self, a_xy: tuple, b_xy: tuple, color=(155, 155, 155), width=1):
        a = Cube(*self.hex_math.xy_id_to_qr(*a_xy))
        b = Cube(*self.hex_math.xy_id_to_qr(*b_xy))

        self.draw_ray_from_a_to_b(a_qr=a, b_qr=b, color=color, width=width)

    def draw_ray_from_a_to_b(self, a_qr: Cube, b_qr: Cube, color=(155, 155, 155), width=1):
        if (a_qr.qrs, b_qr.qrs) not in self.cached_rays:
            self.cached_rays[(a_qr.qrs, b_qr.qrs)] = HexMath.ray_from_a_to_b(a_qr, b_qr)
        ray = self.cached_rays[(a_qr.qrs, b_qr.qrs)]

        if ray:
            ray = [self.get_real_center_of_tile_qr(qr) for qr in ray]
            if len(ray) >= 2:
                draw.lines(Global.display, color, False, ray, width)
            else:
                draw.line(Global.display, color, *ray, width)

    def set_scale(self, scale: float):
        if scale > self.MAX_SCALE:
            self.scale = self.MAX_SCALE
        else:
            self.scale = scale
        self.reload_surface()
