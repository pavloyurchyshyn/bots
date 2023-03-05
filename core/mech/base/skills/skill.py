from typing import Iterable
from abc import abstractmethod
# from core.game_logic.game_data import GameGlobal
from core.mech.base.skills.constants import Targets
from core.mech.base.skills.exceptions import SpellWithoutNameError, TargetsTypeNotDefined


class BaseSkill:
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

    def is_valid_target(self, target: str) -> bool:
        return target in self.targets

    def update_cd(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    @abstractmethod
    def use(self, **kwargs) -> dict:
        raise NotImplementedError

    @property
    def on_cooldown(self) -> bool:
        return self.cooldown_value > 0

    # def clear_use(self):
    #     self.use_dict.clear()
