import json
import os
from typing import List, Dict
from settings.base import MAPS_SAVES
from core.world.base.logic.world import LogicWorld
from core.world.base.constants import TileDataAbs, EmptyTile, TileTypes


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
                tile = world.xy_to_tile[x, y]
                if tile.name != EmptyTile.name:
                    line.append(world.xy_to_tile[x, y].get_data_dict())
                else:
                    line.append(0)

    return map_data


def dict_to_tile_data(data: dict) -> TileDataAbs:
    return TileTypes.types_dict.get(data['name'])(**data)


def list_to_world(data: List[List[dict]]) -> List[List[TileDataAbs]]:
    map_data = []
    for y, line in enumerate(data):
        new_line = []
        map_data.append(new_line)
        for x, tile_data in enumerate(line):
            if tile_data:
                tile_data = dict_to_tile_data(tile_data)
                new_line.append(tile_data)
            else:
                new_line.append(EmptyTile())

    return map_data


# TODO add tests


def save_world(path: str, w: LogicWorld) -> None:
    with open(os.path.join(MAPS_SAVES, f"{path}.json"), 'w') as f:
        json.dump(world_to_list(w), f)


def load_world(map_name: str) -> List[List[TileDataAbs]]:
    map_name = map_name if map_name.endswith('.json') else f"{map_name}.json"
    with open(os.path.join(MAPS_SAVES, map_name), 'r') as f:
        return list_to_world(json.load(f))


def load_available_maps() -> Dict[str, List[List[TileDataAbs]]]:
    maps = {}
    for map_name in os.listdir(MAPS_SAVES):
        maps[map_name.split('.')[0]] = load_world(map_name)

    return maps