from abc import abstractmethod
from typing import Optional, Tuple, Dict, List, Callable
from core.mech.mixins import MechPropertiesMixin, MechParameterCalculationMixin
from core.mech.details.body import BaseBody
from core.mech.details.detail import BaseDetail
from core.mech.details.slot import BaseSlot
from core.mech.skills.skill import BaseSkill


class MechAbs(MechPropertiesMixin, MechParameterCalculationMixin):
    body: BaseBody
    _position: Optional[Tuple[int, int]]
    _left_slots: Dict[int, BaseSlot]
    _right_slots: Dict[int, BaseSlot]

    _damage: float
    _armor: float
    _hp: float
    _hp_regen: float
    _energy: float
    _energy_regen: float

    _current_hp: float
    _current_energy: float

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