from typing import Iterable
from abc import abstractmethod
from global_obj.logger import get_logger
from core.mech.skills.constants import Targets
from core.mech.skills.exceptions import SpellWithoutNameError, TargetsTypeNotDefined


class BaseSkillInterface:
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
        pass

    def update_base_attrs(self, attrs: dict) -> None:
        pass

    def update_cd(self):
        pass

    @abstractmethod
    def use(self, **kwargs) -> dict:
        """
        Do action.
        """
        raise NotImplementedError

    @property
    def on_cooldown(self) -> bool:
        pass

    @abstractmethod
    def get_dict(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def update_attrs(self, attr: dict) -> None:
        raise NotImplementedError

    def validate_use(self, player, world, details_pool, players, **kwargs) -> bool:
        pass
