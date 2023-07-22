from typing import Union, List, Tuple
from core.world.base.logic.tile import LogicTile
from core.world.base.logic.tiles_data import TileDataAbs, TileTypes
from core.world.base.hex_utils import Cube, XYIdHex, HexMath, HexSizes


class VisualTile(LogicTile, HexSizes):
    def __init__(self, xy_id: tuple[int, int],
                 radius: int,
                 # dots: List[Tuple[int, int]],
                 # texture_size: Tuple[int, int],
                 # center: Tuple[int, int],
                 tile_data: Union[str, TileDataAbs] = None,
                 at_edge: bool = False
                 ):
        tile_data = tile_data if tile_data else TileTypes.Forest
        super().__init__(xy_id, tile_data, at_edge=at_edge)
        HexSizes.__init__(self, radius)

        # self.center = center
        center = self.center
        self.texture_size = self.size[0], self.size[0]
        dy = self.hex_width - self.hex_height  # TODO do prettier
        self.texture_pos = center[0] - self.texture_size[0] // 2, center[1] - (self.texture_size[1] + dy)//2 - 1
        # self.lt_pos = center[0] - texture_size[0], center[1] - texture_size[1]
        #
        # self.dots: List[Tuple[int, int]] = dots
        # self.texture_size: Tuple[int, int] = texture_size

