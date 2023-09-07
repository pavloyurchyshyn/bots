import os
from pathlib import Path
from typing import Dict, Union
from pygame import Surface, draw
from global_obj.logger import get_logger
from visual.UI.utils import get_surface, load_image
LOGGER = get_logger()


class TexturePack:
    ERROR_TEXTURE = get_surface(231, 200, 1, color=(200, 0, 0, 0))

    def __init__(self, path: Union[str, Path], pack_name: str = None):
        self.path: Path = Path(path)
        self.name: str = pack_name if pack_name else Path(path).name
        self.textures: Dict[str, Surface] = {}
        self.load(self.path)

    def get_texture(self, *args, raise_error: bool = False) -> Surface:
        path = Path(*args).as_posix()
        if path in self.textures:
            return self.textures[path]
        else:
            LOGGER.debug(f'Missing texture: {path}')
            keys = tuple(filter(lambda key: key.startswith(path), self.textures.keys()))
            if keys:
                return self.textures[keys[0]]
            else:
                LOGGER.warning(f'Returns error texture {path}')  # TODO warn
                if raise_error:
                    raise FileNotFoundError(path)
                return self.ERROR_TEXTURE

    def load(self, parent_path):
        for file in os.listdir(parent_path):
            path = Path(parent_path, file)
            if path.is_file():
                if path.suffix in ('.png', '.jpeg'):
                    path = path.as_posix()
                    LOGGER.debug(f'Loading texture: {path}')
                    self.load_img(path)
            else:
                self.load(path)

    def load_img(self, path: str) -> None:
        k = path.split(self.name)[-1].replace(Path(path).suffix, '')
        self.textures[k] = load_image(path)

    def __str__(self):
        return str(self.textures)


if __name__ == '__main__':
    from settings.base import TEXTURES_FOLDER
    from settings.common import get_texture_pack_name

    tp = TexturePack(TEXTURES_FOLDER / get_texture_pack_name())
    print(tp.name)
    print(tp.path)
    print(Path('1', '', '2'))
