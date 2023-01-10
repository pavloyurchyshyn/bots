import random
from core.world.base.map_save import MapSave


class GameSettings:
    def __init__(self, seed=random.getrandbits(32),
                 planing_time=-10,
                 prepare_time=-20,
                 time_per_step=-10,
                 inventory_size=5,
                 actions_count=3,
                 default_details=None,
                 max_players_num=2,
                 details_pool_settings=None,
                 default_details_settings=None
                 ):
        self.details = {}
        self.planing_time = planing_time
        self.prepare_time = prepare_time
        self.time_per_step = time_per_step
        self.inventory_size = inventory_size
        self.actions_count = actions_count
        self.default_details = default_details
        self.seed = seed
        self.max_players_num = max_players_num
        self.details_pool_settings = {} if details_pool_settings is None else details_pool_settings  # DEFAULT_DETAILS_POOL_SETTINGS.copy()
        self.default_details_settings = {} if default_details_settings is None else default_details_settings  # DEFAULT_START_DETAILS.copy()

        self.game_map: MapSave = None

    def dict(self):
        return dict(seed=self.seed,
                    planing_time=self.planing_time,
                    prepare_time=self.prepare_time,
                    time_per_step=self.time_per_step,
                    inventory_size=self.inventory_size,
                    actions_count=self.actions_count,
                    default_details=self.default_details,
                    max_players_num=self.max_players_num,
                    details_pool_settings=self.details_pool_settings,
                    default_details_settings=self.default_details_settings)

    def add_detail(self, detail_name: str):
        self.details[detail_name] = self.details.get(detail_name, 0) + 1

    def minus_detail(self, detail_name: str):
        if self.details.get(detail_name, 0) != 0:
            self.details[detail_name] = self.details.get(detail_name, 0) - 1

    def set_detail_count(self, detail_name: str, number: int):
        self.details[detail_name] = number
