import os
from pathlib import Path
from pygame import Surface, transform
from typing import Tuple, Dict, Union, List
from pygame.draw import polygon as d_polygon, lines as d_lines
from settings.base import DEFAULT_TEXTURES_FOLDER, TEXTURES_FOLDER
from core.shape.hex import Hex
from settings.tile_settings import TileSettings
from visual.UI.utils import get_surface, load_image
from visual.hex_stuff import rotate_hex
from global_obj.logger import get_logger
from core.world.base.logic.tile import LogicTile
# TODO clean
LOGGER = get_logger()


class TextureByPath:
    def __init__(self, path: Path, flat: bool = True):
        self.path: str = path
        self.flat: bool = flat
        self.images: Dict[Tuple[Tuple[int, int], int], Surface] = {}
        self.original_img: Surface = self.load_img(path, flat)

    def get_texture(self, size, direction: '0-5' = 0) -> Surface:
        if (size, direction) not in self.images:
            if direction != 0:
                img = transform.rotate(self.original_img, direction * 80)
            else:
                img = self.original_img

            self.images[(size, direction)] = transform.smoothscale(img, size)

        return self.images[(size, direction)]

    @staticmethod
    def load_img(path: str, flat: bool) -> Surface:
        LOGGER.debug(f'Loading: {path} {"flat" if flat else "point"}')
        if flat:
            return load_image(path)
        else:
            return transform.rotate(load_image(path), 30)

    def reload(self):
        self.original_img = self.load_img(self.path, self.flat)
        self.images[(self.original_img.get_size(), 0)] = self.original_img


class TextureGroup:
    """Same as folder"""

    def __init__(self, tag: str):
        self.tag = tag
        self.textures_dict: Dict[str, TextureByPath] = {}
        self.textures: List[TextureByPath] = []

    def get_texture_by_num(self, num: int):
        if len(self.textures) <= num:
            return self.textures[0]
        else:
            return self.textures[num]

    def add(self, texture: TextureByPath):
        self.textures_dict[texture.path] = texture
        self.textures.append(texture)

    def remove(self, texture: TextureByPath):
        self.textures_dict.pop(texture.path, None)
        if texture in self.textures:
            self.textures.remove(texture)


class TilesTextures:
    def __init__(self):
        self.textures: Dict[str, TextureByPath] = {}
        self.textures_groups: Dict[str, TextureGroup] = {}
        self.load_textures()

    def load_textures(self, folder: Path = None):
        if folder is None:
            folder = DEFAULT_TEXTURES_FOLDER
        elif not folder.exists():
            folder = TEXTURES_FOLDER / folder

        tiles = folder / 'tiles'
        for tile_type in os.listdir(tiles):
            self.textures_groups[tile_type] = texture_group = TextureGroup(tile_type)
            for img in os.listdir(tiles / tile_type):
                texture = TextureByPath(tiles / tile_type / img)
                texture_group.add(texture)
                self.textures[texture.path] = texture

    def get_texture(self, tile: LogicTile) -> TextureByPath:
        return self.textures_groups[tile.name]

    # def get_texture(self, path: str or Path) -> TextureByPath:
    #     if path not in self.textures:
    #         if not Path(path).exists():
    #             LOGGER.error(f'Loading texture which doesnt exist: {path}')
    #         self.textures[path] = TextureByPath(path)
    #     return self.textures[path]

    def clear(self):
        self.textures_groups.clear()


if __name__ == '__main__':
    TilesTextures()
