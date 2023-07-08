from typing import List, Optional, Tuple, Union, Dict
from core.entities.effects.base import BaseEffect
from core.entities.entity_abc import BaseEntityAbc


class EffectsManager:
    def __init__(self, entity: Optional[Union[BaseEntityAbc, 'BaseEntity']] = None, effects: Optional[List[BaseEffect]] = None):
        self.entity: BaseEntityAbc = self if entity is None else entity
        self.effects: List[BaseEffect] = effects if effects else []
        self.effects_dict: Dict[str, BaseEffect] = {}

    def apply_effects(self):
        for effect in self.effects:
            effect.affect()

    def add_effect(self, effect: BaseEffect):
        self.effects.append(effect)
        self.effects_dict[effect.uid] = effect

    def remove_effect(self, effect: BaseEffect):
        if effect in self.effects:
            self.effects.remove(effect)
        self.effects_dict.pop(effect.uid)

    def do_effects_tick(self):
        for effect in self.effects.copy():
            effect.tick()
            if effect.not_active:
                effect.on_end()
                self.remove_effect(effect=effect)

    def get_effects_by_type(self, type_: str) -> Tuple['BaseEffect']:
        return tuple(filter(lambda effect: type_ in effect.types, self.effects))

    def get_effect_by_uid(self, uid: str) -> Optional[BaseEffect]:
        return self.effects_dict.get(uid)

    def get_effects_by_types(self, types: Tuple[str]) -> Tuple['BaseEffect']:
        effects = set()
        for type_ in types:
            effects.update(self.get_effects_by_type(type_=type_))
        return tuple(effects)

    @property
    def positive_effects(self) -> Tuple['BaseEffect']:
        return tuple(filter(lambda effect: effect.is_positive, self.effects))

    @property
    def negative_effects(self) -> Tuple['BaseEffect']:
        return tuple(filter(lambda effect: effect.is_negative, self.effects))
