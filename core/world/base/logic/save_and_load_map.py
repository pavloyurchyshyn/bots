from typing import List
from core.world.base.logic.world import LogicWorld
from core.world.base.constants import TileDataAbs, EmptyTile


def world_to_list(world: LogicWorld) -> List[List[dict]]:
    """
    Returns list with tiles dict data
    """
    map_data = []

    for y in range(world.y_size):
        line = []
        map_data.append(line)
        for x in range(world.x_size):
            if (x, y) in world.xy_to_tile:
                line.append(world.xy_to_tile[x, y].get_data_dict())

    return map_data


def dict_to_tile_data(data: dict) -> TileDataAbs:
    return TileDataAbs(**data)


def list_to_world(data: List[List[dict]]) -> List[List[TileDataAbs]]:
    map_data = []
    for y, line in enumerate(data):
        new_line = []
        map_data.append(new_line)
        for x, tile_data in enumerate(line):
            tile_data = dict_to_tile_data(tile_data)
            if tile_data:
                new_line.append(tile_data)
            else:
                new_line.append(EmptyTile())

    return map_data
# TODO add tests