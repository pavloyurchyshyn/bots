import os
import datetime
from typing import List
from settings.base import MAPS_SAVES
from core.world.base.map_save import MapSave
from core.world.classic_maps.forest import ForestMap


class MapsManager:
    def __init__(self):
        self.maps: List[MapSave] = []

    def load_maps(self):
        self.maps.clear()
        for map_save in os.listdir(MAPS_SAVES):
            save = MapSave()
            save.load_save_from_file(os.path.join(MAPS_SAVES, map_save))
            self.maps.append(save)
        self.load_default_maps()
        self.sort()

    def load_default_maps(self):
        self.maps.append(ForestMap())

    def add_map(self, map_save: MapSave):
        self.maps.append(map_save)

    def delete(self, map_save: MapSave):
        if not map_save.default:
            map_save.delete()
            self.maps.remove(map_save)

    def load_from_dict(self, data: List[dict]):
        for data_ in data:
            self.maps.append(MapSave(**data_.pop('metadata'), **data_))

    def sort(self):
        self.maps.sort(key=lambda m: m.name)
