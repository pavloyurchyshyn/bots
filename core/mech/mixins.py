from typing import List, Tuple
from core.mech.skills.skill import BaseSkill
from core.mech.details.constants import DetailsAttrs


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
    def skills(self) -> List[BaseSkill]:
        return self._skills

    @property
    def position(self):
        return tuple(self._position)

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
        self._damage = self.get_collected_damage()

    def get_collected_damage(self) -> float:
        return self._collect_parameter_value_from_details(DetailsAttrs.Damage)
    def calculate_armor(self):
        self._armor = self.get_collected_armor()

    def get_collected_armor(self) -> float:
        return self._collect_parameter_value_from_details(DetailsAttrs.Armor)

    def calculate_hp(self):
        self._hp = self.get_collected_hp()

    def get_collected_hp(self) -> float:
        return self._collect_parameter_value_from_details(DetailsAttrs.AddHP)
    def calculate_hp_regen(self):
        self._hp_regen = self.get_collected_hp_regen()

    def get_collected_hp_regen(self) -> float:
        return self._collect_parameter_value_from_details(DetailsAttrs.HPRegen)

    def calculate_energy(self):
        self._energy = self.get_collected_energy()

    def get_collected_energy(self) -> float:
        return self._collect_parameter_value_from_details(DetailsAttrs.AddEnergy)
    def calculate_energy_regen(self):
        self._energy_regen = self.get_collected_energy_regen()

    def get_collected_energy_regen(self) -> float:
        return self._collect_parameter_value_from_details(DetailsAttrs.EnergyRegen)
    def _collect_parameter_value_from_details(self, part_attr):
        v = 0
        for detail in self.details:
            v += getattr(detail, part_attr, 0)
        v += getattr(self.body, part_attr, 0)
        return v


class EffectsMixin:
    _effects: List['BaseEffect']

    @property
    def positive_effects(self) -> Tuple['BaseEffect']:
        return tuple(filter(lambda effect: effect.is_positive, self._effects))

    @property
    def negative_effects(self) -> Tuple['BaseEffect']:
        return tuple(filter(lambda effect: effect.is_negative, self._effects))

    def add_effect(self, effect: 'BaseEffect') -> None:
        self._effects.append(effect)

    def delete_effect(self, effect: 'BaseEffect'):
        if effect in self._effects:
            self._effects.remove(effect)

    def do_effects_tick(self):
        for effect in self._effects.copy():
            effect.tick()
            if effect.not_active:
                self.delete_effect(effect=effect)

    def get_effects_by_type(self, type_: str) -> Tuple['BaseEffect']:
        return tuple(filter(lambda effect: type_ in effect.types, self._effects))

    def get_effects_by_types(self, types: Tuple[str]) -> Tuple['BaseEffect']:
        effects = set()
        for type_ in types:
            effects.update(self.get_effects_by_type(type_=type_))
        return tuple(effects)

    def apply_effects(self):
        for effect in self._effects:
            effect.affect(mech=self)

    # def on_damage_events(self):
    # def on_move_events(self):
    # def on_shoot_events(self):
    # def on_death_events(self):
    # def on_mech_kill_events(self):
    # def on_npc_kill_events(self):
    # def on_undefined_actions_events(self):
