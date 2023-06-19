from typing import Tuple, Union
from core.entities.entity_abc import BaseEntityAbc


class PositiveNotDefinedError(Exception):
    pass


class TypesNotDefinedError(Exception):
    pass


class NoNameDefinedError(Exception):
    pass


class BaseEffect:
    types: Tuple[str] = None
    is_positive: bool = None
    keep_after_death: bool = False
    permanent: bool = False

    name: str = None
    verbal_name: str = None

    def __init__(self, dealer: Union['BaseEntityAbc', 'BaseEntity'], target: Union['BaseEntityAbc', 'BaseEntity'], duration: int):
        if self.name is None or self.verbal_name is None:
            raise NoNameDefinedError

        if self.types is None:
            raise TypesNotDefinedError

        if self.is_positive is None:
            raise PositiveNotDefinedError

        self.dealer: 'BaseEntityAbc' = dealer
        self.target: 'BaseEntityAbc' = target
        self.duration: int = round(duration)

    def tick(self):
        if self.permanent:
            return
        self.duration -= 1

    @property
    def active(self) -> bool:
        return self.permanent or self.duration > 0

    @property
    def not_active(self) -> bool:
        return not self.active

    def affect(self):
        self.target.effects_manager.add_effect(self)

    def on_end(self):
        self.target.effects_manager.remove_effect(self)

    @property
    def is_negative(self) -> bool:
        return self.is_positive
