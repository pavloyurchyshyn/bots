import os
from pygame import Surface
from pygame.draw import polygon as d_polygon, lines as d_lines
from settings.base import TILES_TEXTURES_FOLDER
from core.shape.hex import Hex
from settings.tile_settings import TileSettings
from visual.UI.utils import get_surface, load_image
from visual.hex_stuff import rotate_hex


class TilesTextures:
    def __init__(self):
        self.textures: dict = {}

    def get_texture(self, path: str, direction: int = 0) -> Surface:
        if path not in self.textures:
            self.textures[(path, direction)] = rotate_hex(load_image(path), direction)


if __name__ == '__main__':
    TilesTextures()
