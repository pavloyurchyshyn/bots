import json
import os
import datetime
from typing import List, Dict
from settings.base import MAPS_SAVES
from core.world.base.logic.world import LogicWorld
from core.world.base.constants import TileDataAbs, EmptyTile, TileTypes
from core.world.base.map_save import MapSave
from core.world.classic_maps.forest import ForestMap


class MapsManager:
    def __init__(self):
        self.maps: List[MapSave] = []
        self.maps.append(ForestMap())
        self.load_maps()
        self.sort()

    def load_maps(self):
        for map_save in os.listdir(MAPS_SAVES):
            save = MapSave(path=os.path.join(MAPS_SAVES, map_save))
            save.set_name_from_path()
            self.maps.append(save)

    def add_map(self, map_save: MapSave):
        self.maps.append(map_save)

    def delete(self, map_save: MapSave):
        if map_save.can_be_deleted:
            map_save.delete()
            self.maps.remove(map_save)

    def sort(self):
        self.maps.sort(key=lambda m: m.name)


if __name__ == '__main__':
    print(str(datetime.datetime.now()))
