import random


class GameSettings:
    def __init__(self):
        self.details = {}
        self.planing_time = -10
        self.prepare_time = -20
        self.time_per_step = -10
        self.inventory_size = 5
        self.actions_count = 3
        self.default_details = None
        self.seed = random.getrandbits(32)
        self.max_players_num = 2
        self.details_pool_settings = {}  # DEFAULT_DETAILS_POOL_SETTINGS.copy()
        self.default_details_settings = {}  # DEFAULT_START_DETAILS.copy()

    def add_detail(self, detail_name: str):
        self.details[detail_name] = self.details.get(detail_name, 0) + 1

    def minus_detail(self, detail_name: str):
        if self.details.get(detail_name, 0) != 0:
            self.details[detail_name] = self.details.get(detail_name, 0) - 1

    def set_detail_count(self, detail_name: str, number: int):
        self.details[detail_name] = number
