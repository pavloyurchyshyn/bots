from abc import abstractmethod
# from core.game_logic.game_data import GameGlobal
from core.mech.base.skills.constants import Targets
from core.mech.base.exceptions import SpellWithoutName, TargetsTypeNotDefined


class BaseSkill:
    """
    Just logic without visual, description etc.
    """
    Targets = Targets
    # StepsClock = GameGlobal.steps_clock
    name = None
    verbal_name = None
    targets = None

    def __init__(self, num, unique_id: str, energy_cost: int, cooldown: int = 1):
        if self.name is None or self.verbal_name is None:
            raise SpellWithoutName

        if self.targets is None:
            raise TargetsTypeNotDefined

        self.unique_id = f'{num}_{unique_id}_{self.name}'

        self.energy_cost = energy_cost
        self.cooldown_value = cooldown
        self.cooldown = 0

    def update_cd(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    @abstractmethod
    def use(self, *args, **kwargs) -> dict:
        raise NotImplementedError

    def on_cooldown(self):
        return self.cooldown_value > 0
