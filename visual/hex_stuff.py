from pygame import draw, Surface, transform
from core.shape.hex import Hex
from settings.tile_settings import TileSettings
from visual.UI.utils import get_surface

__prepared_hex = Hex(0, 0, TileSettings.visual_tile_r)


def get_colored_hex(color, surface=None, dots=__prepared_hex.dots[1:]) -> Surface:
    surface = surface if surface else get_surface(__prepared_hex.width + 1, __prepared_hex.height + 1, 1)
    return draw_hex(surface, color, dots)


def rotate_hex(surface: Surface, direction: int) -> Surface:
    return transform.rotate(surface, direction * 30)


def draw_hex_border(surface, color, dots=__prepared_hex.dots[1:], width=1) -> Surface:
    draw.lines(surface, color, True, dots, width)
    return surface


def draw_hex(surface, color, dots=__prepared_hex.dots[1:], width=0) -> Surface:
    draw.polygon(surface, color, dots, width)
    draw.line(surface, (255, 0, 0), __prepared_hex.dots[0], (__prepared_hex.dots[0][0], 0), 5)
    return surface
