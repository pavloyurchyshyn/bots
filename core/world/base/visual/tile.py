from typing import Union, List, Tuple
from core.world.base.logic.tile import LogicTile
from core.world.base.constants import TileDataAbs, IMPASSABLE_VALUE, TileTypes


class VisualTile(LogicTile):
    def __init__(self, xy_id: tuple[int, int],
                 dots: List[Tuple[int, int]],
                 tile_data: Union[str, TileDataAbs] = None):
        tile_data = tile_data if tile_data else TileTypes.Field
        super().__init__(xy_id, tile_data)
        self.dots: List[Tuple[int, int]] = dots
