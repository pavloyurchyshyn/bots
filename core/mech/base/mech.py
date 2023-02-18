from core.mech.base.details.body import BaseBody
from core.mech.base.exceptions import SlotDoesntExistsError, WrongDetailType
from core.mech.base.skills.exceptions import NotEnoughEnergyError
from core.mech.base.details.constants import DetailsAttrs, MechAttrs, DetailsTypes


class MechPropertiesMixin:
    @property
    def health_regen(self):
        return self._hp_regen

    @property
    def full_energy(self):
        return self._energy

    @property
    def energy(self):
        return self._current_energy

    @property
    def health_points(self):
        return self._current_hp

    @property
    def energy_regen(self):
        return self._energy_regen

    @property
    def damage(self):
        return self._damage

    @property
    def armor(self):
        return self._armor

    @property
    def full_health_points(self):
        return self._hp

    @property
    def skills(self):
        return self._skills

    @property
    def position(self):
        return self._position

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


class MechParameterCalculationMixin:
    def calculate_attrs(self):
        self.calculate_damage()
        self.calculate_armor()
        self.calculate_hp()
        self.calculate_hp_regen()
        self.calculate_energy()
        self.calculate_energy_regen()

    def calculate_damage(self):
        self._damage = self._calculate_parameter(DetailsAttrs.Damage)

    def calculate_armor(self):
        self._armor = self._calculate_parameter(DetailsAttrs.Armor)

    def calculate_hp(self):
        self._hp = self._calculate_parameter(DetailsAttrs.AddHP)

    def calculate_hp_regen(self):
        self._hp_regen = self._calculate_parameter(DetailsAttrs.HPRegen)

    def calculate_energy(self):
        self._energy = self._calculate_parameter(DetailsAttrs.AddEnergy)

    def calculate_energy_regen(self):
        self._energy_regen = self._calculate_parameter(DetailsAttrs.EnergyRegen)

    def _calculate_parameter(self, part_attr):
        v = 0
        for detail in self.details:
            v += getattr(detail, part_attr, 0)
        v += getattr(self.body, part_attr, 0)
        return v


class BaseMech(MechPropertiesMixin, MechParameterCalculationMixin):
    """
    This is an object which contains body and calculating attrs.
    Body contains other details.
    """

    def __init__(self, position, body_detail: BaseBody = None):
        self.body = body_detail

        self._position = position

        # - slots -
        self._left_slots = {}
        self._right_slots = {}
        self.build_slots()
        # ----------

        self._damage = 0
        self._armor = 0
        self._hp = 0
        self._hp_regen = 0
        self._energy = 0
        self._energy_regen = 0

        self.calculate_attrs()
        self._current_hp = self._hp
        self._current_energy = self._energy

        self._skills = []
        self.collect_abilities()

    def update_details_and_attrs(self):
        self.build_slots()
        self.calculate_attrs()
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

    def change_position(self, pos):
        self._position = pos

    def set_left_detail(self, slot_id, detail):
        self.set_detail(self._left_slots, slot_id, detail)

    def set_right_detail(self, slot_id, detail):
        self.set_detail(self._right_slots, slot_id, detail)

    def set_detail(self, slots: dict, slot_id, detail, update_attr=True):
        if slots.get(slot_id):
            slots[slot_id].set_detail(detail)
            if update_attr:
                self.update_details_and_attrs()
        else:
            raise SlotDoesntExistsError(f'{slot_id} in {slots}')

    def switch_part(self, slots, slot_id, detail, update_attr=True):
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

    def deal_damage(self, dmg):
        self._current_hp -= dmg

    def have_enough_energy(self, energy) -> bool:
        return self._current_energy - energy >= 0.

    def spend_energy(self, energy):
        if energy > self._current_energy:
            raise NotEnoughEnergyError

        self._current_energy -= energy

    def set_max_hp(self):
        self._current_hp = self._hp

    def set_health_points(self, hp):
        self._current_hp = hp

    def set_max_energy(self):
        self._current_energy = self._energy

    def set_energy(self, energy):
        self._current_energy = energy

    def attr_dict(self):
        return {
            DetailsAttrs.Damage: self._damage,
            DetailsAttrs.Armor: self._armor,
            DetailsAttrs.AddHP: self._hp,
            DetailsAttrs.HPRegen: self._hp_regen,
            DetailsAttrs.AddEnergy: self._energy,
            DetailsAttrs.EnergyRegen: self._energy_regen,
            MechAttrs.Position: self._position,
            MechAttrs.CurrentHP: self._current_hp,
            MechAttrs.CurrentEnergy: self._current_energy,
        }

    def set_attrs(self, data: dict):
        for key, attr in (
                (DetailsAttrs.Damage, '_damage'),
                (DetailsAttrs.Armor, '_armor'),
                (DetailsAttrs.AddHP, '_hp'),
                (MechAttrs.Position, '_position'),
                (DetailsAttrs.HPRegen, '_hp_regen'),
                (DetailsAttrs.AddEnergy, '_energy'),
                (DetailsAttrs.EnergyRegen, '_energy_regen'),
                (MechAttrs.CurrentHP, '_current_hp'),
                (MechAttrs.CurrentEnergy, '_current_energy'),
        ):
            setattr(self, attr, data[key] if data.get(key) is not None else getattr(self, attr))
