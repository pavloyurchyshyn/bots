from typing import List, Optional, Tuple
from core.entities.base.effects.base import BaseEffect

class EffectsManager:
    def __init__(self, entity: Optional['BaseEntity'] = None, effects: Optional[List[BaseEffect]] = None):
        self.entity: 'BaseEntity' = self if entity is None else entity
        self.effects: List[BaseEffect] = effects if effects else []

    def apply_effects(self):
        for effect in self.effects:
            effect.affect()

    def add_effect(self, effect: BaseEffect):
        self.effects.append(effect)

    def remove_effect(self, effect: BaseEffect):
        if effect in self.effects:
            self.effects.remove(effect)

    def do_effects_tick(self):
        for effect in self.effects.copy():
            effect.tick()
            if effect.not_active:
                self.remove_effect(effect=effect)

    def get_effects_by_type(self, type_: str) -> Tuple['BaseEffect']:
        return tuple(filter(lambda effect: type_ in effect.types, self.effects))

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
