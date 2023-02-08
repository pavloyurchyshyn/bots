import os
from core.shape.hex import Hex
from pathlib import Path
from pygame import Surface, transform, draw
from typing import Tuple, Dict, Union, List
from visual.UI.utils import get_surface, load_image


class TexturePack:
    ERROR_TEXTURE = get_surface(231, 200, 1, color=(0, 0, 0, 0))
    draw.polygon(ERROR_TEXTURE, (200, 0, 0), Hex(0, 0, 115).dots[1:])

    def __init__(self, path: Union[str, Path], pack_name: str = None):
        self.path: Path = Path(path)
        self.name: str = pack_name if pack_name else Path(path).name
        self.textures: Dict[str, Surface] = {}
        self.load(self.path)

    def get_texture(self, *args) -> Surface:
        return self.textures.get(Path(*args).as_posix(), self.ERROR_TEXTURE)

    def load(self, parent_path):
        for file in os.listdir(parent_path):
            path = Path(parent_path, file)
            if path.is_file():
                if path.suffix in ('.png', '.jpeg'):
                    path = path.as_posix()
                    self.load_img(path)
            else:
                self.load(path)

    def load_img(self, path: str) -> None:
        self.textures[path.split('.')[0].replace(self.path.as_posix(), '')] = load_image(path)

    def __str__(self):
        return str(self.textures)


if __name__ == '__main__':
    from settings.base import TEXTURES_FOLDER
    from settings.common import get_texture_pack

    tp = TexturePack(TEXTURES_FOLDER / get_texture_pack())
    print(tp.name)
    print(tp.path)
    print(Path('1', '', '2'))
