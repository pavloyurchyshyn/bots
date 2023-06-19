from typing import Callable, List, Type, Optional


class Attr:
    def __init__(self, base: float, current: float,
                 name: Optional[str] = None,
                 base_multiplier: float = 0, multiplier: float = 0,
                 base_additional: float = 0, additional: float = 0,
                 multipliers_functions: List[Callable] = None,
                 additionals_functions: List[Callable] = None,
                 ):
        self.name: Optional[str] = name
        self.base: float = base
        self.current: float = current

        self.base_multiplier: float = base_multiplier
        self.base_additional: float = base_additional

        self.multiplier: float = multiplier
        self.additional: float = additional

        self.dynamic_multipliers_functions: List[Callable] = multipliers_functions if multipliers_functions else []
        self.dynamic_additionals_functions: List[Callable] = additionals_functions if additionals_functions else []

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
        return sum(map(lambda f: f(attr=self, *args, **kwargs), self.dynamic_additionals_functions))

    def add_multiplayer_func(self, func: Callable) -> None:
        self.dynamic_multipliers_functions.append(func)

    def delete_multiplayer_func(self, func: Callable) -> None:
        if func in self.dynamic_multipliers_functions:
            self.dynamic_multipliers_functions.remove(func)

    def add_additional_func(self, func: Callable) -> None:
        self.dynamic_additionals_functions.append(func)

    def delete_additional_func(self, func: Callable) -> None:
        if func in self.dynamic_additionals_functions:
            self.dynamic_additionals_functions.remove(func)

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

    def deal_damage(self, dmg: float):
        self._hp -= dmg

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
