from typing import List, Tuple, Dict, Type
from core.world.base.logic.tile import LogicTile, TileDataAbs
from core.world.base.constants import EmptyTile


class LogicWorld:

    def __init__(self, tile_class=Type[LogicTile]):
        self.tile_class: tile_class = tile_class
        self.flat = self.odd = True
        self.y_size = None
        self.x_size = None
        self.tiles: List[LogicTile] = []
        self.xy_to_tile: Dict[Tuple[int, int], LogicTile] = {}

    def add_tile(self, tile: LogicTile):
        self.tiles.append(tile)
        self.xy_to_tile[(tile.id_x, tile.id_y)] = tile

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
                if tile_data:
                    self.add_tile(self.get_tile_from_data(x, y, tile_data))
                else:
                    self.add_tile(self.get_tile_from_data(x, y, EmptyTile()))

    def clear(self):
        self.tiles.clear()
        self.xy_to_tile.clear()

    def get_tile_from_data(self, x, y, tile_data: TileDataAbs, **extra_data) -> LogicTile:
        return self.tile_class(xy_id=(x, y), tile_data=tile_data, **extra_data)

    # def get_map_data(self) -> List[List[Type[TileDataAbs]]]:
    #     map_data = []
    #     for y in range(self.y_size):
    #         line = []
    #         map_data.append(line)
    #         for x in range(self.x_size):
    #             if (x, y) in self.xy_to_tile:
    #                 line.append(self.xy_to_tile[x, y].get_data_dict())
    #
    #     return map_data
