from typing import Iterable, Callable
from abc import abstractmethod
from global_obj.logger import get_logger
from core.validators.skill import SkillsValidations
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
                 target_validation_func: Callable,
                 energy_cost: int,
                 health_points_cost: int = 0,
                 validators: tuple = (),
                 cooldown: int = 1,
                 current_cooldown: int = 0,
                 cast_range: int = 1):
        if self.name is None or self.verbal_name is None:
            raise SpellWithoutNameError

        if self.targets is None:
            raise TargetsTypeNotDefined

        self.unique_id = f'{num}_{unique_id}_{self.name}'

        self.energy_cost = energy_cost
        self.health_points_cost = health_points_cost
        self.cooldown_value = cooldown
        self.cooldown = current_cooldown
        self.cast_range: int = cast_range
        self.validators = (
            SkillsValidations.no_empty_slots,
            SkillsValidations.player_owns_skill_by_uid,
            SkillsValidations.skill_not_on_cooldown,
            SkillsValidations.player_has_enough_of_energy,
            target_validation_func,
            SkillsValidations.target_in_range,
            *validators)

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

    def set_on_cooldown(self, value=None):
        self.cooldown = value if value else self.cooldown_value

    # TODO add decorator to wrap in events
    @abstractmethod
    def use(self, skill_cast_uid: str, player, game_obj, target_xy, mech=None) -> None:
        """
        Do action.
        """
        raise NotImplementedError

    @property
    def on_cooldown(self) -> bool:
        return self.cooldown > 0 and not self.get_on_cooldown_cond()

    def get_on_cooldown_cond(self, *_, **__) -> bool:
        """For dynamic things, for example depends on something"""
        return False

    @property
    def not_on_cooldown(self) -> bool:
        return not self.on_cooldown

    @abstractmethod
    def get_dict(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def update_attrs(self, attrs: dict) -> None:
        raise NotImplementedError

    def validate_use(self, player, **kwargs) -> None:
        for validation in self.validators:
            validation(player=player,
                       skill=self,
                       skill_uid=self.unique_id,
                       **kwargs)

    def __str__(self):
        return str(self.name)