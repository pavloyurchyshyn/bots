from typing import Union, List, Tuple
from core.world.base.logic.tile import LogicTile
from core.world.base.logic.tiles_data import TileDataAbs, TileTypes


class VisualTile(LogicTile):
    def __init__(self, xy_id: tuple[int, int],
                 dots: List[Tuple[int, int]],
                 tile_data: Union[str, TileDataAbs] = None,
                 at_edge: bool = False):
        tile_data = tile_data if tile_data else TileTypes.Forest
        super().__init__(xy_id, tile_data, at_edge=at_edge)
        self.dots: List[Tuple[int, int]] = dots

