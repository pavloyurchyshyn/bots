from typing import Tuple, Dict
from pygame import Surface, transform
from global_obj.logger import get_logger
from settings.base import TEXTURES_FOLDER
from settings.common import get_texture_pack_name
from visual.textures.texture_pack import TexturePack
from settings.visual.cards import SkillCardSize


LOGGER = get_logger()


class Textures:
    def __init__(self):
        self.textures_folder = TEXTURES_FOLDER
        self.packs: Dict[str, TexturePack] = {}
        self.pack_hash: Dict[str, Dict[Tuple[str, Tuple[int, int]], Surface]] = {}

    def get_card_texture(self, img: str, size: Tuple[int, int] = SkillCardSize.SIZE) -> Surface:
        return self.get_texture_with_size(path=f'/cards/{img}', size=size)

    def get_tile_texture(self, tile_type: str, img: str) -> Surface:
        return self.current_pack.get_texture('tiles', str(tile_type), str(img))

    def get_scaled_tile_texture(self, tile_type: str, img: str, size: Tuple[int, int], raise_error: bool = False):
        return self.get_texture_with_size(f'/tiles/{tile_type}/{img}', size, raise_error=raise_error)

    def get_texture_with_size(self, path: str, size: Tuple[int, int], raise_error: bool = False):
        k = (path, size)
        self.pack_hash[get_texture_pack_name()] = pack_hash = self.pack_hash.get(get_texture_pack_name(), {})
        if k not in pack_hash:
            surface = self.current_pack.get_texture(path, raise_error=raise_error)
            pack_hash[k] = transform.smoothscale(surface, size)
        return pack_hash[k]

    @property
    def current_pack(self):
        pack_name = get_texture_pack_name()
        if pack_name not in self.packs:
            LOGGER.info(f'Loading "{pack_name}" texture pack.')
            self.packs[pack_name] = TexturePack(self.textures_folder / pack_name)

        return self.packs[pack_name]

    def clear(self):
        self.packs.clear()
        self.pack_hash.clear()


#

if __name__ == '__main__':
    tp = Textures()
    print(tp.current_pack)
