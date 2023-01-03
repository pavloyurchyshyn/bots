import json
import os
import datetime
from typing import List
from settings.base import MAPS_SAVES
from core.world.base.logic.world import LogicWorld
from core.world.base.constants import TileDataAbs, EmptyTile, TileTypes


def get_world_dict_structure(name: str, tiles_data: List[List[dict]], created: str) -> dict:
    return {
        'name': name,
        'metadata': {
            'created': created
        },
        'tiles_data': tiles_data,
    }


class MapSave:
    def __init__(self, name: str = '', path: str = '',
                 tiles_data: List[List[TileDataAbs]] = None,
                 can_be_deleted: bool = True,
                 can_be_saved: bool = True,
                 dict_tiles_data: List[List[dict]] = None):
        self.__name: str = name
        self.__path = path if path else self.get_map_path(name) if name else ''
        self.__tiles_data: List[List[TileDataAbs]] = tiles_data
        self.__json_tiles_data: List[List[dict]] = [[]] if dict_tiles_data is None else dict_tiles_data
        self.__can_be_deleted = can_be_deleted
        self.__can_be_saved = can_be_saved

    def get_tiles_data(self):
        if not self.__tiles_data:
            self.__tiles_data = self.json_data_to_tiles_data(self.__json_tiles_data)
        return self.__tiles_data

    def load(self):
        data = self.load_json_data_from_file(self.__path)
        self.__name = data['name']
        self.__json_tiles_data = data['tiles_data']

    def save(self, forced=False):
        if not self.can_be_saved:
            return

        if os.path.exists(self.__path):
            if forced:
                self.delete_map(self.__path)
            else:
                raise FileExistsError(self.__path)
        self.save_json_data_to_file(self.__path, self.get_save_dict())

    def delete(self):
        if self.can_be_deleted:
            self.delete_map(self.__path)

    @property
    def can_be_saved(self):
        return self.can_be_saved

    @staticmethod
    def delete_map(map_path: str) -> None:
        os.remove(map_path)

    @property
    def name(self):
        return self.__name

    @property
    def can_be_deleted(self) -> bool:
        return self.__can_be_deleted

    @staticmethod
    def get_map_path(map_name: str) -> str:
        map_name = map_name.lower().replace(' ', '_')
        return os.path.join(MAPS_SAVES, map_name if map_name.endswith('.json') else f"{map_name}.json")

    def set_name_from_path(self) -> None:
        self.__name = self.path_to_name(self.__path)

    @staticmethod
    def path_to_name(path: str) -> str:
        path = os.path.basename(path)
        return path.replace('.json', '').replace('_', ' ').capitalize()

    @staticmethod
    def load_json_data_from_file(map_path: str) -> dict:
        with open(map_path, 'r') as f:
            return json.load(f)

    @staticmethod
    def save_json_data_to_file(map_path: str, data: dict) -> None:
        with open(map_path, 'w') as f:
            json.dump(data, f)

    def get_save_dict(self) -> dict:
        if not self.__name or not self.__json_tiles_data:
            raise Exception

        return get_world_dict_structure(self.__name,
                                        self.__json_tiles_data,
                                        created=str(datetime.datetime.now()))

    def save_as_raw_text(self):
        with open(self.__path.replace('.json', '.txt'), 'w') as f:
            f.write(str(self.get_save_dict()))

    @staticmethod
    def json_data_to_tiles_data(data: List[List[dict]]) -> List[List[TileDataAbs]]:
        map_data = []
        for y, line in enumerate(data):
            new_line = []
            map_data.append(new_line)
            for x, tile_data in enumerate(line):
                if tile_data:
                    new_line.append(MapSave.get_tile_type(tile_data))
                else:
                    new_line.append(EmptyTile())

        return map_data

    @staticmethod
    def world_to_json_data(world: LogicWorld) -> List[List[dict]]:
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

    @staticmethod
    def get_tile_type(data: dict) -> TileDataAbs:
        return TileTypes.types_dict.get(data['name'])(**data)
