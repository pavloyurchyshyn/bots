from pygame import Surface, transform
from typing import Union, List, Tuple
from global_obj.main import Global
from core.world.base.logic.tile import LogicTile
from core.world.base.logic.tiles_data import TileDataAbs, TileTypes, EmptyTile
from visual.tiles_textures import TextureGroup, ERROR_TEXTURE


class VisualTile(LogicTile):
    def __init__(self, xy_id: tuple[int, int],
                 dots: List[Tuple[int, int]],
                 texture_size: Tuple[int, int],
                 center: Tuple[int, int],
                 tile_data: Union[str, TileDataAbs] = None,
                 at_edge: bool = False
                 ):
        tile_data = tile_data if tile_data else TileTypes.Forest
        super().__init__(xy_id, tile_data, at_edge=at_edge)
        self.center = center
        self.texture_pos = center[0] - texture_size[0] // 2, center[1] - texture_size[1] // 2
        self.lt_pos = center[0] - texture_size[0], center[1] - texture_size[1]

        self.dots: List[Tuple[int, int]] = dots
        self.texture_size: Tuple[int, int] = texture_size
        self.texture: Surface = None
        if self.name != EmptyTile.name:
            self.load_texture()

    def load_texture(self):
        texture_mngr = self.texture_mngr.get_texture_by_num(self.img)
        self.texture = texture_mngr.get_texture(self.texture_size)

    def apply_type(self, tile_type: Union[str, TileDataAbs]) -> None:
        super().apply_type(tile_type)
        self.load_texture()

    @property
    def texture_mngr(self) -> TextureGroup:
        return Global.tiles_textures.get_texture_group(self)
