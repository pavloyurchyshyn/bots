from typing import Callable, List, Type, Optional
from core.world.base.logic.tile import LogicTile
from core.mech.skills.skill import BaseSkill


class Attr:
    def __init__(self, base: float, current: float,
                 name: Optional[str] = None,
                 base_multiplier: float = 0, multiplier: float = 0,
                 base_additional: float = 0, additional: float = 0,
                 multipliers_functions: List[Callable] = None,
                 additional_functions: List[Callable] = None,
                 ):
        self.name: Optional[str] = name
        self.base: float = base
        self.current: float = current

        self.base_multiplier: float = base_multiplier
        self.base_additional: float = base_additional

        self.multiplier: float = multiplier
        self.additional: float = additional

        self.dynamic_multipliers_functions: List[Callable] = multipliers_functions if multipliers_functions else []
        self.dynamic_additional_functions: List[Callable] = additional_functions if additional_functions else []

    def set_multiplayer(self, value: float) -> None:
        self.multiplier = value

    def add_multiplayer(self, value: float) -> None:
        self.multiplier += value

    def minus_multiplayer(self, value: float) -> None:
        self.multiplier -= value

    def set_value(self, value: float) -> None:
        self.additional = value

    def add_value(self, value: float) -> None:
        self.additional += value

    def minus_value(self, value: float) -> None:
        self.additional -= value

    def update_current(self):
        self.current = self.dynamic_current

    @property
    def dynamic_current(self) -> float:
        add = self.base_additional + self.additional + self.get_dynamic_additional()
        mul = self.base_multiplier + self.multiplier + self.get_dynamic_multiplayer()
        return self.base + self.base * mul + add

    def get_added_value(self) -> float:
        return self.base_additional + self.additional + self.get_dynamic_additional()

    def get_multiplied_value(self) -> float:
        mul = self.base_multiplier + self.multiplier + self.get_dynamic_multiplayer()
        return (self.base * mul) - self.base

    def get_dynamic_multiplayer(self, *args, **kwargs) -> float:
        return sum(map(lambda f: f(attr=self, *args, **kwargs), self.dynamic_multipliers_functions))

    def get_dynamic_additional(self, *args, **kwargs) -> float:
        return sum(map(lambda f: f(attr=self, *args, **kwargs), self.dynamic_additional_functions))

    def add_multiplayer_func(self, func: Callable) -> None:
        self.dynamic_multipliers_functions.append(func)

    def delete_multiplayer_func(self, func: Callable) -> None:
        if func in self.dynamic_multipliers_functions:
            self.dynamic_multipliers_functions.remove(func)

    def add_additional_func(self, func: Callable) -> None:
        self.dynamic_additional_functions.append(func)

    def delete_additional_func(self, func: Callable) -> None:
        if func in self.dynamic_additional_functions:
            self.dynamic_additional_functions.remove(func)


class EntityAttrs:
    CurrentV = 'c'
    BaseV = 'b'

    Id: str = 'unique_id'
    Damage: str = 'damage'
    Armor: str = 'armor'
    AddHP: str = 'add_hp'
    HPRegen: str = 'hp_regen'  # regeneration
    AddEnergy: str = 'add_energy'
    EnergyRegen: str = 'energy_regen'

    Position: str = 'position'
    CurrentHP: str = 'current_hp'
    CurrentEnergy: str = 'current_energy'
    MaxHP = 'max_hp'
    MaxEnergy = 'max_energy'

    Luck: str = 'luck'
    AddRange: str = 'add_range'
    SkillUseEnrgK: str = 'skill_use_enrg_k'
    MoveEnrgK: str = 'move_energy_k'
    HealK: str = 'heal_k'
    PosEffectsDurK = 'pos_eff_dur'
    NegEffectsDurK = 'neg_eff_dur'
    Attrs = 'attrs'


class EntityBaseAttrsPart:
    AttrsDict = {
        EntityAttrs.Damage: 'damage_attr',
        EntityAttrs.Armor: 'armor_attr',
        EntityAttrs.HPRegen: 'hp_regen_attr',
        EntityAttrs.EnergyRegen: 'energy_regen_attr',

        EntityAttrs.MaxHP: 'max_hp_attr',
        EntityAttrs.MaxEnergy: 'max_energy_attr',

        EntityAttrs.CurrentHP: '_hp',
        EntityAttrs.CurrentEnergy: '_energy',
        EntityAttrs.Position: 'position',

        EntityAttrs.Luck: 'luck',
        EntityAttrs.AddRange: 'additional_range',
        EntityAttrs.SkillUseEnrgK: 'move_energy_k',
        EntityAttrs.MoveEnrgK: 'additional_range',
        EntityAttrs.HealK: 'heal_k',
        EntityAttrs.PosEffectsDurK: 'pos_effects_duration',
        EntityAttrs.NegEffectsDurK: 'neg_effects_duration',

    }

    def __init__(self,
                 current_hp: float = 0,
                 max_hp: float = 0, current_max_hp: float = 0,
                 hp_regen: float = 0, current_hp_regen: float = 0,

                 current_energy: float = 0,
                 max_energy: float = 0, current_max_energy: float = 0,
                 energy_regen: float = 0, current_energy_regen: float = 0,
                 damage: float = 0, current_damage: float = 0,
                 armor: float = 0, current_armor: float = 0,

                 luck: int = 1, current_luck: int = 1,
                 skill_use_energy_k: int = 1, current_skill_use_energy_k: int = 1,
                 move_energy_k: int = 1, current_move_energy_k: int = 1,
                 heal_k_base: int = 1, heal_k_current: int = 1,
                 positive_effect_duration_k_base: int = 1, positive_effect_duration_k_current: int = 1,  # TODO
                 negative_effect_duration_k_base: int = 1, negative_effect_duration_k_current: int = 1,

                 additional_range_attr_base=0,
                 additional_range_attr_current=0,

                 attrs_class: Type[Attr] = Attr,
                 ):
        self._hp: float = current_hp
        self.max_hp_attr: Attr = attrs_class(base=max_hp, current=current_max_hp)
        self.hp_regen_attr: Attr = attrs_class(base=hp_regen, current=current_hp_regen)

        self._energy: float = current_energy
        self.max_energy_attr: Attr = attrs_class(base=max_energy, current=current_max_energy)
        self.energy_regen_attr: Attr = attrs_class(base=energy_regen, current=current_energy_regen)

        self.damage_attr: Attr = attrs_class(base=damage, current=current_damage)
        self.armor_attr: Attr = attrs_class(base=armor, current=current_armor)

        self.luck_attr: Attr = attrs_class(base=luck, current=current_luck)

        self.additional_range_attr: Attr = attrs_class(base=additional_range_attr_base,
                                                       current=additional_range_attr_current)
        self.skill_use_energy_k_attr: Attr = attrs_class(base=skill_use_energy_k, current=current_skill_use_energy_k)
        self.move_energy_k_attr: Attr = attrs_class(base=move_energy_k, current=current_move_energy_k)
        self.heal_k_attr: Attr = attrs_class(base=heal_k_base, current=heal_k_current)  # skill heal value * attr%

        self.positive_effect_duration_k_attr: Attr = attrs_class(base=positive_effect_duration_k_base,  # TODO
                                                                 current=positive_effect_duration_k_current)
        self.negative_effect_duration_k_attr: Attr = attrs_class(base=negative_effect_duration_k_base,
                                                                 current=negative_effect_duration_k_current)

    @property
    def luck(self) -> float:
        return int(self.luck_attr.dynamic_current)

    @property
    def additional_range(self) -> int:
        return int(self.additional_range_attr.dynamic_current)

    @property
    def skill_use_k(self) -> float:
        return self.skill_use_energy_k_attr.dynamic_current

    @property
    def heal_k(self) -> float:
        return self.heal_k_attr.dynamic_current

    @property
    def move_energy_k(self) -> float:
        return self.move_energy_k_attr.dynamic_current

    def deal_damage(self, dmg: float):
        self._hp -= dmg

    def have_enough_energy(self, energy: float) -> bool:
        return self._energy - energy >= 0.

    def spend_energy_on_skill_use(self, skill: BaseSkill, allow_minus: bool = False):
        self.spend_energy(energy=skill.energy_cost * self.skill_use_k, allow_minus=allow_minus)

    def spend_energy_on_move(self, skill: BaseSkill, tile: LogicTile, allow_minus: bool):
        self.spend_energy(energy=(tile.move_energy_k + self.move_energy_k) * skill.energy_cost, allow_minus=allow_minus)

    def spend_energy(self, energy: float, allow_minus: bool = False):
        # TODO think
        # if energy > self._energy and not allow_minus:
        #     raise NotEnoughEnergyError

        self._energy -= energy

    def set_health_points(self, hp: float):
        self._hp = hp

    def set_energy(self, energy: float):
        self._energy = energy

    def refresh_hp(self):
        self._hp = self.max_hp_attr.dynamic_current

    def refresh_energy(self):
        self._energy = self.max_energy_attr.dynamic_current

    @property
    def health_points(self) -> float:
        return self._hp

    @property
    def max_health_point(self) -> float:
        return self.max_hp_attr.dynamic_current

    @property
    def health_regen(self) -> float:
        return self.hp_regen_attr.dynamic_current

    @property
    def energy(self) -> float:
        return self._energy

    @property
    def max_energy(self) -> float:
        return self.max_energy_attr.dynamic_current

    @property
    def energy_regen(self) -> float:
        return self.energy_regen_attr.dynamic_current

    @property
    def damage(self) -> float:
        return self.damage_attr.dynamic_current

    @property
    def armor(self) -> float:
        return self.armor_attr.dynamic_current

    @property
    def pos_effects_duration(self):
        return self.positive_effect_duration_k_attr.dynamic_current

    @property
    def neg_effects_duration(self):
        return self.negative_effect_duration_k_attr.dynamic_current
