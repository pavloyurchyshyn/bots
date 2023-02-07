from typing import List, Tuple, Dict, Type
from core.world.base.logic.tile import LogicTile, TileDataAbs
from core.world.base.logic.tiles_data import EmptyTile


class LogicWorld:

    def __init__(self, tile_class: LogicTile = LogicTile):
        self.tile_class: LogicTile = tile_class
        self.flat = self.odd = True
        self.y_size = None
        self.x_size = None
        self.tiles: List[LogicTile] = []
        self.xy_to_tile: Dict[Tuple[int, int], LogicTile] = {}

    def get_tile_by_xy(self, xy):
        return self.xy_to_tile.get(xy)

    def add_tile(self, tile: LogicTile):
        self.tiles.append(tile)
        self.xy_to_tile[(tile.id_x, tile.id_y)] = tile

    def remove_tile_by_xy(self, xy: tuple):
        if xy in self.xy_to_tile:
            self.remove_tile(self.xy_to_tile.get(xy))

    def remove_tile(self, tile: LogicTile):
        self.xy_to_tile.pop((tile.id_x, tile.id_y), None)
        if tile in self.tiles:
            self.tiles.remove(tile)

    def change_tile(self, tile: LogicTile):
        if (tile.id_x, tile.id_y) in self.xy_to_tile:
            self.tiles.remove(self.xy_to_tile[(tile.id_x, tile.id_y)])

        self.add_tile(tile)

    def build_map(self, flat, odd, data: List[List[TileDataAbs]]):
        self.flat = flat
        self.odd = odd
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

    def get_tile_from_data(self, x, y, tile_data: TileDataAbs, **extra_data) -> LogicTile:
        return self.tile_class(xy_id=(x, y), tile_data=tile_data, **extra_data)
