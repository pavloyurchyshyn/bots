from typing import Tuple, Union, Dict
from core.entities.entity_abc import BaseEntityAbc
from core.mech.skills.abs import BaseSkillInterface
from core.entities.effects.constants import SerializeConst


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

    def __init__(self, uid: str, dealer: Union['BaseEntityAbc', 'BaseEntity'],
                 target: Union['BaseEntityAbc', 'BaseEntity'],
                 parent_skill: Union[BaseSkillInterface, 'BaseSkill'],
                 duration: int,
                 serializing: bool = False):
        if not serializing and (self.name is None or self.verbal_name is None):
            raise NoNameDefinedError

        if not serializing and self.types is None:
            raise TypesNotDefinedError

        if not serializing and self.is_positive is None:
            raise PositiveNotDefinedError
        self.uid: str = uid
        self.dealer: 'BaseEntityAbc' = dealer
        self.target: 'BaseEntityAbc' = target
        self.parent_skill: BaseSkillInterface = parent_skill
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
        self.add_to_target()

    def add_to_target(self):
        self.target.effects_manager.add_effect(self)

    def on_end(self):
        self.remove_from_target()

    def remove_from_target(self):
        self.target.effects_manager.remove_effect(self)

    @property
    def is_negative(self) -> bool:
        return self.is_positive

    def get_dict(self) -> Dict[str, str | int]:
        return {
            SerializeConst.Name: self.name,
            SerializeConst.UID: self.uid,
            SerializeConst.Target: self.target.uid,
            SerializeConst.Dealer: self.dealer.uid,
            SerializeConst.Types: self.types,
            SerializeConst.KeepAfterDeath: self.keep_after_death,
            SerializeConst.ParentSkill: self.parent_skill.unique_id,
            SerializeConst.Duration: self.duration,
            SerializeConst.IsPositive: self.is_positive,
        }
