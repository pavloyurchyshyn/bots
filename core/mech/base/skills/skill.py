from typing import Iterable
from abc import abstractmethod
from global_obj.logger import get_logger
from core.mech.base.skills.constants import Targets, SkillAttrs
from core.mech.base.skills.exceptions import SpellWithoutNameError, TargetsTypeNotDefined


class BaseSkill:
    logger = get_logger()
    """
    Just logic without visual, description etc.
    """
    TargetsConst = Targets
    name: str = None
    verbal_name: str = None
    targets: Iterable = None

    def __init__(self, num, unique_id: str, energy_cost: int, validators: list, cooldown: int = 1):
        if self.name is None or self.verbal_name is None:
            raise SpellWithoutNameError

        if self.targets is None:
            raise TargetsTypeNotDefined

        self.unique_id = f'{num}_{unique_id}_{self.name}'

        self.energy_cost = energy_cost
        self.cooldown_value = cooldown
        self.cooldown = 0
        self.validators = validators

    def get_base_dict(self) -> dict:
        return {
            SkillAttrs.UID: self.unique_id,
            SkillAttrs.CD: self.cooldown,
            SkillAttrs.ECost: self.energy_cost,
            SkillAttrs.OnCD: self.on_cooldown,
        }

    def update_base_attrs(self, attr: dict) -> None:
        self.cooldown = attr.get(SkillAttrs.CD, self.cooldown)
        self.energy_cost = attr.get(SkillAttrs.ECost, self.energy_cost)

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

    @abstractmethod
    def get_dict(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def update_attrs(self, attr: dict) -> None:
        raise NotImplementedError

    def validate_use(self, player, world, details_pool, players, **kwargs) -> bool:
        for validation in self.validators:
            if not validation(player=player, world=world,
                              details_pool=details_pool,
                              players=players, skill=self,
                              skill_uid=self.unique_id,
                              **kwargs):
                return False

        return True
