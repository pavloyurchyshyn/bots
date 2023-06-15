from copy import deepcopy
from typing import List, Dict, Optional
from core.mech.details.body import BaseBody
from core.mech.details.detail import BaseDetail
from core.mech.details.slot import BaseSlot
from core.mech.skills.skill import BaseSkill

from core.entities.base.entity import BaseEntity
from core.entities.base.effects.base import BaseEffect


from core.mech.exceptions import SlotDoesntExistsError, WrongDetailType
from core.mech.details.constants import DetailsAttrs, MechAttrs, DetailsTypes


class BaseMech(BaseEntity):
    """
    This is an object which contains body and calculating attrs.
    Body contains other vanilla_details.
    """
    AttrsDict = {
        DetailsAttrs.Damage: 'damage_attr',
        DetailsAttrs.Armor: 'armor_attr',
        DetailsAttrs.HPRegen: 'hp_regen_attr',
        DetailsAttrs.EnergyRegen: 'energy_regen_attr',

        MechAttrs.MaxHP: 'max_hp_attr',
        MechAttrs.MaxEnergy: 'max_energy_attr',

        MechAttrs.CurrentHP: '_hp',
        MechAttrs.CurrentEnergy: '_energy',
        MechAttrs.Position: 'position',
    }

    def __init__(self, position,
                 body_detail: BaseBody = None,
                 attrs_kwargs: dict = None,
                 effects: Optional[List[BaseEffect]] = None):
        attrs_kwargs = {} if attrs_kwargs is None else attrs_kwargs
        super().__init__(position=position, **attrs_kwargs, effects=effects)
        self.body: BaseBody = body_detail

        # - slots -
        self._left_slots: Dict[int, BaseSlot] = {}
        self._right_slots: Dict[int, BaseSlot] = {}
        self.build_slots()
        # ----------

        self.collect_base_attrs()

        self._skills: List[BaseSkill] = []
        self.collect_abilities()

    def refill_energy_and_hp(self):
        self.refresh_hp()
        self.refresh_energy()

    def update_details_and_attrs(self):
        self.build_slots()
        self.collect_base_attrs()
        self.collect_abilities()

    def set_body(self, body: BaseBody):
        if body.detail_type != BaseBody.detail_type:
            raise WrongDetailType(body, BaseBody.detail_type)

        self.body = body
        self.build_slots()

    def drop_body(self) -> BaseBody:
        b = self.body
        self.body = None
        return b

    def build_slots(self):
        if self.body:
            self.__build_slots(self._left_slots, self.body.get_left_slots())
            self.__build_slots(self._right_slots, self.body.get_right_slots())
        else:
            self._left_slots.clear()
            self._right_slots.clear()

    def __build_slots(self, side: dict, slots: tuple):
        old_slots = side.copy()
        side.clear()
        slots = (slot() for slot in slots)
        slots = sorted(slots, key=lambda s: DetailsTypes.LEG_TYPE in s.types)
        for i, slot in enumerate(slots):
            if i in old_slots and old_slots[i].is_full:
                slot.set_detail(old_slots[i].get_and_clear())

            side[i] = slot

    def set_left_detail(self, slot_id: int, detail: BaseDetail):
        self.set_detail(self._left_slots, slot_id, detail)

    def set_right_detail(self, slot_id: int, detail: BaseDetail):
        self.set_detail(self._right_slots, slot_id, detail)

    def set_detail(self, slots: dict, slot_id: int, detail: BaseDetail, update_attr=True):
        if slots.get(slot_id) is not None:
            slots[slot_id].set_detail(detail)
            if update_attr:
                self.update_details_and_attrs()
        else:
            raise SlotDoesntExistsError(f'{slot_id} in {slots}')

    def switch_part(self, slots: dict, slot_id: int, detail: BaseDetail, update_attr=True):
        slot = slots.get(slot_id)
        if slot:
            d = slot.switch_detail(detail)
            if update_attr:
                self.update_details_and_attrs()
            return d
        else:
            raise SlotDoesntExistsError(slot_id)

    def collect_abilities(self):
        self._skills.clear()
        if self.body:
            self._skills.extend(self.body.skills)
            for detail in self.details:
                self._skills.extend(detail.skills)

    def have_enough_energy(self, energy: float) -> bool:
        return self._energy - energy >= 0.

    def spend_energy(self, energy: float, allow_minus: bool = False):
        # TODO think
        # if energy > self._energy and not allow_minus:
        #     raise NotEnoughEnergyError

        self._energy -= energy

    def set_health_points(self, hp: float):
        self._hp = hp

    def set_energy(self, energy: float):
        self._energy = energy

    def attr_dict(self):
        # TODO add base and current
        return {
            MechAttrs.Position: self._position.xy_id,
            MechAttrs.CurrentHP: self._hp,
            MechAttrs.CurrentEnergy: self._energy,

            MechAttrs.MaxHP: {DetailsAttrs.BaseV: self.max_hp_attr.base,
                              DetailsAttrs.CurrentV: self.max_hp_attr.dynamic_current},
            DetailsAttrs.HPRegen: {DetailsAttrs.BaseV: self.hp_regen_attr.base,
                                   DetailsAttrs.CurrentV: self.hp_regen_attr.dynamic_current},

            MechAttrs.MaxEnergy: {DetailsAttrs.BaseV: self.max_energy_attr.base,
                                  DetailsAttrs.CurrentV: self.max_energy_attr.dynamic_current},
            DetailsAttrs.EnergyRegen: {DetailsAttrs.BaseV: self.energy_regen_attr.base,
                                       DetailsAttrs.CurrentV: self.energy_regen_attr.dynamic_current},

            DetailsAttrs.Damage: {DetailsAttrs.BaseV: self.damage_attr.base,
                                  DetailsAttrs.CurrentV: self.damage_attr.dynamic_current},
            DetailsAttrs.Armor: {DetailsAttrs.BaseV: self.armor_attr.base,
                                 DetailsAttrs.CurrentV: self.armor_attr.dynamic_current},

        }

    def set_attrs(self, data: dict):
        for key, attr_value in data.items():
            attr = self.AttrsDict.get(key)
            if attr is None or attr_value is None:
                # TODO add logger
                continue
            if key == MechAttrs.Position:
                self._position = self.get_position_obj(data.get(key, self.position))
            elif key in (MechAttrs.CurrentHP, MechAttrs.CurrentEnergy):
                setattr(self, attr, attr_value)
            else:
                getattr(self, attr).base = attr_value.get(DetailsAttrs.BaseV, getattr(self, attr).base)
                getattr(self, attr).current = attr_value.get(DetailsAttrs.CurrentV, getattr(self, attr).dynamic_current)

    def get_details(self) -> List[BaseDetail]:
        return [slot.detail for slot in [*self._left_slots.values(), *self._right_slots.values()] if slot.is_full]

    def __str__(self):
        return str(self.attr_dict())

    def make_empty(self):
        self._skills.clear()
        self._left_slots.clear()
        self._right_slots.clear()
        self.body = None

    def get_copy(self) -> 'BaseMech':
        return deepcopy(self)

    @property
    def skills(self) -> List[BaseSkill]:
        return self._skills

    @property
    def details(self):
        p = []
        for side in (self._left_slots, self._right_slots):
            for slot in side.values():
                if slot.is_full:
                    p.append(slot.detail)

        return p

    @property
    def left_slots(self):
        return self._left_slots

    @property
    def right_slots(self):
        return self._right_slots


    def collect_base_attrs(self):
        self.calculate_damage()
        self.calculate_armor()
        self.calculate_max_hp()
        self.calculate_hp_regen()
        self.calculate_max_energy()
        self.calculate_energy_regen()

    def calculate_damage(self):
        self.damage_attr.base = self.get_collected_damage()

    def get_collected_damage(self) -> float:
        return self._collect_parameter_value_from_details(DetailsAttrs.Damage)

    def calculate_armor(self):
        self.armor_attr.base = self.get_collected_armor()

    def get_collected_armor(self) -> float:
        return self._collect_parameter_value_from_details(DetailsAttrs.Armor)

    def calculate_max_hp(self):
        self.max_hp_attr.base = self.get_collected_max_hp()

    def get_collected_max_hp(self) -> float:
        return self._collect_parameter_value_from_details(DetailsAttrs.AddHP)

    def calculate_hp_regen(self):
        self.hp_regen_attr.base = self.get_collected_hp_regen()

    def get_collected_hp_regen(self) -> float:
        return self._collect_parameter_value_from_details(DetailsAttrs.HPRegen)

    def calculate_max_energy(self):
        self.max_energy_attr.base = self.get_collected_max_energy()

    def get_collected_max_energy(self) -> float:
        return self._collect_parameter_value_from_details(DetailsAttrs.AddEnergy)

    def calculate_energy_regen(self):
        self.energy_regen_attr.base = self.get_collected_energy_regen()

    def get_collected_energy_regen(self) -> float:
        return self._collect_parameter_value_from_details(DetailsAttrs.EnergyRegen)

    def _collect_parameter_value_from_details(self, part_attr):
        v = 0
        for detail in self.details:
            v += getattr(detail, part_attr, 0)
        v += getattr(self.body, part_attr, 0)
        return v