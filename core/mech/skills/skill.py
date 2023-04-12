from typing import Iterable
from abc import abstractmethod
from global_obj.logger import get_logger
from core.mech.skills.constants import Targets, SkillAttrs
from core.mech.skills.exceptions import SpellWithoutNameError, TargetsTypeNotDefined


class BaseSkill:
    logger = get_logger()
    """
    Just logic without visual, description etc.
    """
    TargetsConst = Targets
    name: str = None
    verbal_name: str = None
    targets: Iterable = None

    def __init__(self, num, unique_id: str,
                 energy_cost: int, validators: tuple,
                 cooldown: int = 1, cast_range: int = 0):
        if self.name is None or self.verbal_name is None:
            raise SpellWithoutNameError

        if self.targets is None:
            raise TargetsTypeNotDefined

        self.unique_id = f'{num}_{unique_id}_{self.name}'

        self.energy_cost = energy_cost
        self.cooldown_value = cooldown
        self.cooldown = 0
        self.cast_range: int = cast_range
        self.validators = validators

    def get_base_dict(self) -> dict:
        return {
            SkillAttrs.UID: self.unique_id,
            SkillAttrs.CD: self.cooldown,
            SkillAttrs.ECost: self.energy_cost,
            SkillAttrs.OnCD: self.on_cooldown,
            SkillAttrs.Range: self.cast_range,
        }

    def update_base_attrs(self, attrs: dict) -> None:
        self.cooldown = attrs.get(SkillAttrs.CD, self.cooldown)
        self.energy_cost = attrs.get(SkillAttrs.ECost, self.energy_cost)

    def update_cd(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    @abstractmethod
    def use(self, **kwargs) -> dict:
        """
        Do action.
        """
        raise NotImplementedError

    @property
    def on_cooldown(self) -> bool:
        return self.cooldown_value > 0

    @property
    def not_on_cooldown(self) -> bool:
        return not self.on_cooldown

    @abstractmethod
    def get_dict(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def update_attrs(self, attr: dict) -> None:
        raise NotImplementedError

    def validate_use(self, player, world, details_pool, players, **kwargs) -> None:
        for validation in self.validators:
            validation(player=player,
                       world=world,
                       details_pool=details_pool,
                       players=players, skill=self,
                       skill_uid=self.unique_id,
                       **kwargs)
