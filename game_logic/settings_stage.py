from typing import Dict, Optional
from core.world.base.map_save import MapSave
from core.world.maps_manager import MapsManager
from game_logic.game_data.game_settings import GameSettings


class SettingsStage:
    def __init__(self):
        self.settings: GameSettings = GameSettings()
        self.maps_mngr: MapsManager = MapsManager()
        self.maps_mngr.load_maps()
        self.chosen_map: int = 0
        self.current_map: MapSave = self.maps_mngr.maps[0]
        self.players_slots: Dict[int, Optional[str]] = {i: None for i in range(self.current_map.spawns_amount)}

    def recreate_slots(self):
        self.players_slots = {i: self.players_slots.get(i) for i in range(self.current_map.spawns_amount)}

    def slot_is_free(self, slot_number: int):
        return self.players_slots[slot_number] is None

    def free_slot(self, slot_number: int):
        if slot_number in self.players_slots:
            self.players_slots[slot_number] = None

    def get_slot(self, slot: int) -> Optional[str]:
        return self.players_slots[slot]

    def set_slot(self, slot: int, token: str):
        if slot in self.players_slots:
            self.players_slots[slot] = token

    def build_slots(self, slots_num: int):
        old_slots = self.players_slots
        self.players_slots = {i: old_slots.get(i) for i in range(slots_num)}

    def set_seed(self, seed: int):
        self.settings.seed = seed

    def set_planing_time(self, time_: int):
        self.settings.planing_time = time_

    def set_prepare_time(self, time_: int):
        self.settings.prepare_time = time_

    def set_time_pre_step(self, time_: int):
        self.settings.time_per_step = time_

    def set_actions_count(self, value_: int):
        self.settings.actions_count = value_

    def set_max_players_num(self, value_: int):
        self.settings.max_players_num = value_

    # details_pool_settings=None,
    # default_details_settings=None
