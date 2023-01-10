import json
import os
import copy
import datetime
from typing import List
from global_obj import Global
from settings.base import MAPS_SAVES
from core.world.base.logic.world import LogicWorld
from core.world.base.logic.tiles_data import TileDataAbs, EmptyTile, TileTypes, TileAttrs


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
                 odd: bool = True, flat: bool = True,
                 dict_tiles_data: List[List[dict | int | None]] = None,
                 default=False):
        self.default = default
        self.__odd = odd
        self.__flat = flat
        self.__name: str = name
        if self.default:
            self.__path = ''
        else:
            self.__path = path if path else self.get_map_path(name) if name else ''
        self.__tiles_data: List[List[TileDataAbs]] = tiles_data

        self.__dict_tiles_data: List[List[dict]] = [[]] if dict_tiles_data is None else dict_tiles_data

    @property
    def size(self):
        return len(self.__dict_tiles_data[0]), len(self.__dict_tiles_data),

    def load_save_from_file(self, path: str):
        data = self.load_json_data_from_file(path)
        self.__name = data['name']
        self.__path = path
        self.__dict_tiles_data = data['tiles_data']

    @property
    def json_tiles_data(self):
        return self.__dict_tiles_data

    def get_tiles_data(self) -> List[List[TileDataAbs]]:
        if not self.__tiles_data:
            self.__tiles_data = self.json_data_to_tiles_data(self.__dict_tiles_data)
        return self.__tiles_data

    def load(self):
        data = self.load_json_data_from_file(self.__path)
        self.__name = data['name']
        self.__dict_tiles_data = data['tiles_data']

    def save(self, forced=False):
        if self.default:
            return

        if os.path.exists(self.__path):
            if forced:
                self.delete_map(self.__path)
            else:
                raise FileExistsError(self.__path)
        self.save_json_data_to_file(self.__path, self.get_save_dict())

    def delete(self):
        if not self.default:
            self.delete_map(self.__path)

    @staticmethod
    def delete_map(map_path: str) -> None:
        os.remove(map_path)

    @property
    def name(self):
        return self.__name

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
        if not self.__name or not self.__dict_tiles_data:
            raise Exception

        return get_world_dict_structure(self.__name,
                                        self.__dict_tiles_data,
                                        created=str(datetime.datetime.now()))

    def save_as_raw_text(self):
        with open(self.__path.replace('.json', '.txt'), 'w') as f:
            f.write(str(self.get_save_dict()))

    def set_world_to_json_data(self, world):
        self.__dict_tiles_data = self.world_to_json_data(world)

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
        return TileTypes.types_dict.get(data[TileAttrs.Name])(**data)

    @property
    def odd(self) -> bool:
        return self.__odd

    @property
    def flat(self) -> bool:
        return self.__flat

    @property
    def path(self) -> str:
        return self.__path

    def copy(self):
        s = MapSave(name=f'{self.__name} copy',
                    odd=self.odd,
                    flat=self.flat,
                    dict_tiles_data=copy.deepcopy(self.__dict_tiles_data),
                    default=False
                    )
        return s

    def set_name(self, name: str):
        self.__name = name
        self.__path = self.get_map_path(name)

    def __eq__(self, other):
        if other:
            return self.__dict__ == other.__dict__
        else:
            return False


if __name__ == '__main__':
    s = MapSave(path='Forest')
    new_s = copy.deepcopy(s)
    print(s, new_s)
    print(s.__dict__)
    print(new_s.__dict__)
    assert s.__dict__ == new_s.__dict__
    assert s == s.copy()
    new_s._MapSave__name = '1'
    assert s != new_s
