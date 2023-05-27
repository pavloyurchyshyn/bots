from typing import List, Tuple, Dict, Type, Optional, Union
from core.world.base.logic.tile import LogicTile, TileDataAbs
from core.world.base.logic.tiles_data import EmptyTile
from core.world.base.hex_utils import HexMath

TileClass = Union[LogicTile, Type[LogicTile]]


class LogicWorld:

    def __init__(self, tile_class: Type[LogicTile] = LogicTile):
        self.tile_class: Type[LogicTile] = tile_class
        self.x_size: int = None
        self.y_size: int = None
        self.tiles: List[LogicTile] = []
        self.xy_to_tile: Dict[Tuple[int, int], TileClass] = {}
        self.qr_to_tile: Dict[Tuple[int, int], TileClass] = {}
        self.hex_math: Type[HexMath] = HexMath

    def get_tile_by_xy(self, xy: Tuple[int, int]) -> Optional[TileClass]:
        return self.xy_to_tile.get(xy)

    def get_tile_by_qr(self, qr: Tuple[int, int]) -> Optional[TileClass]:
        return self.qr_to_tile.get(qr)

    def add_tile(self, tile: TileClass):
        self.tiles.append(tile)
        self.xy_to_tile[tile.xy_id] = tile
        self.qr_to_tile[tile.qr] = tile

    def remove_tile_by_xy(self, xy: Tuple[int, int]):
        if xy in self.xy_to_tile:
            self.remove_tile(self.xy_to_tile[xy])

    def remove_tile_by_qr(self, qr: Tuple[int, int]):
        if qr in self.qr_to_tile:
            self.remove_tile(self.qr_to_tile[qr])

    def remove_tile(self, tile: TileClass):
        self.xy_to_tile.pop(tile.xy_id, None)
        if tile in self.tiles:
            self.tiles.remove(tile)

    def change_tile(self, tile: TileClass):
        if tile.xy_id in self.xy_to_tile:
            self.tiles.remove(self.xy_to_tile[tile.xy_id])

        self.add_tile(tile)

    def build_map(self, data: List[List[TileDataAbs]]):
        self.y_size = len(data)
        self.x_size = len(max(data, key=len))

        for y, line in enumerate(data):
            for x, tile_data in enumerate(line):
                if x == 0 or y == 0 or (y == self.y_size - 1) or (x == self.x_size - 1):
                    at_edge = True
                else:
                    at_edge = False

                if tile_data:
                    self.add_tile(self.get_tile_from_data(x, y, tile_data, at_edge=at_edge))
                else:
                    self.add_tile(self.get_tile_from_data(x, y, EmptyTile(), at_edge=at_edge))

    def clear(self):
        self.tiles.clear()
        self.xy_to_tile.clear()
        self.qr_to_tile.clear()

    def get_tile_from_data(self, x: int, y: int, tile_data: TileDataAbs, **extra_data) -> TileClass:
        return self.tile_class(xy_id=(x, y), tile_data=tile_data, **extra_data)
