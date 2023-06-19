from abc import abstractmethod
from typing import Optional, Tuple, Dict, List, Callable
from core.entities.entity import BaseEntity
from core.mech.details.body import BaseBody
from core.mech.details.detail import BaseDetail
from core.mech.details.slot import BaseSlot
from core.mech.skills.skill import BaseSkill
from core.entities.stats_attrs import Attr

class MechAbs(BaseEntity):
    body: BaseBody
    _left_slots: Dict[int, BaseSlot]
    _right_slots: Dict[int, BaseSlot]

    _hp: float
    max_hp_attr: Attr
    hp_regen_attr: Attr

    _energy: float
    max_energy_attr: Attr
    energy_regen_attr: Attr

    damage_attr: Attr
    armor_attr: Attr

    position: Optional[Tuple[int, int]]

    _skills: List['BaseSkill']

    refill_energy_and_hp: Callable

    update_details_and_attrs: Callable

    @abstractmethod
    def set_body(self, body: BaseBody):
        pass

    @abstractmethod
    def drop_body(self) -> BaseBody:
        pass

    @abstractmethod
    def build_slots(self):
        pass

    @abstractmethod
    def __build_slots(self, side: dict, slots: tuple):
        pass

    @abstractmethod
    def change_position(self, pos: Tuple[int, int]):
        pass

    @abstractmethod
    def set_left_detail(self, slot_id: int, detail: BaseDetail):
        pass

    @abstractmethod
    def set_right_detail(self, slot_id: int, detail: BaseDetail):
        pass

    @abstractmethod
    def set_detail(self, slots: dict, slot_id: int, detail: BaseDetail, update_attr=True):
        pass

    @abstractmethod
    def switch_part(self, slots: dict, slot_id: int, detail: BaseDetail, update_attr=True):
        pass

    @abstractmethod
    def collect_abilities(self):
        pass

    @abstractmethod
    def deal_damage(self, dmg: float):
        pass

    @abstractmethod
    def have_enough_energy(self, energy: float) -> bool:
        pass

    @abstractmethod
    def spend_energy(self, energy: float, allow_minus: bool = False):
        pass

    @abstractmethod
    def set_max_hp(self):
        pass

    @abstractmethod
    def set_health_points(self, hp: float):
        pass

    @abstractmethod
    def set_max_energy(self):
        pass

    @abstractmethod
    def set_energy(self, energy: float):
        pass

    @abstractmethod
    def attr_dict(self) -> dict:
        pass

    @abstractmethod
    def set_attrs(self, data: dict):
        pass

    @abstractmethod
    def get_details(self) -> List[BaseDetail]:
        pass

    def __str__(self):
        return str(self.attr_dict())

    @abstractmethod
    def make_empty(self):
        pass

    @abstractmethod
    def get_copy(self) -> 'BaseMech':
        pass