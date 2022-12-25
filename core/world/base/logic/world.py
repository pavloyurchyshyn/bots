from typing import List, Tuple, Dict
from core.world.base.logic.tile import LogicTile, TileDataAbs


class LogicWorld:

    def __init__(self, tile_class=LogicTile):
        self.tile_class: tile_class = tile_class
        self.flat = self.odd = True
        self.y_size = None
        self.x_size = None
        self.tiles: List[LogicTile] = []
        self.xy_to_tile: Dict[Tuple[int, int], LogicTile] = {}

    def add_tile(self, tile: LogicTile):
        self.tiles.append(tile)
        self.xy_to_tile[(tile.id_x, tile.id_y)] = tile

    def build_map(self, flat, odd, data: List[List[TileDataAbs]]):
        self.flat = flat
        self.odd = odd
        self.y_size = len(data)
        self.x_size = len(max(data, key=len))
        for y, line in enumerate(data):
            for x, tile_data in enumerate(line):
                if tile_data:
                    tile = self.get_tile_from_data(x, y, tile_data)
                    self.add_tile(tile)

    def clear(self):
        self.tiles.clear()
        self.xy_to_tile.clear()

    def get_tile_from_data(self, x, y, tile_data: TileDataAbs, **extra_data) -> LogicTile:
        return self.tile_class(xy_id=(x, y), tile_data=tile_data, **extra_data)
