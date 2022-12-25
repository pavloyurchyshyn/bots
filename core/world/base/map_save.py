import os
import json
from settings.base import MAPS_SAVES


class MapSaveManager:
    @staticmethod
    def load_map(name: str) -> dict:
        if not os.path.exists(os.path.join(MAPS_SAVES, name)):
            raise FileNotFoundError

        return {}

    @staticmethod
    def save_map(name: str, map_data: dict, hard_write=False):
        if os.path.exists(os.path.join(MAPS_SAVES, name)):
            if hard_write:
                os.remove(os.path.join(MAPS_SAVES, name))
            else:
                raise FileExistsError

        with open(os.path.join(MAPS_SAVES, name)) as f:
            json.dump(map_data, f)
