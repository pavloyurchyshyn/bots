from typing import Tuple
from abc import abstractmethod
from core.mech.abs import MechAbs
# from core.player.player import PlayerObj

class PositiveNotDefinedError(Exception):
    pass

class TypesNotDefinedError(Exception):
    pass


class BaseEffect:
    types: Tuple[str] = None
    is_positive: bool = None
    keep_after_death: bool = False
    permanent: bool = False

    def __init__(self, dealer: 'PlayerObj', duration: int):
        if self.types is None:
            raise TypesNotDefinedError

        if self.is_positive is None:
            raise PositiveNotDefinedError

        self.dealer: 'PlayerObj' = dealer
        self.duration: int = duration

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

    @abstractmethod
    def affect(self, mech: MechAbs):
        raise NotImplementedError

    @property
    def is_negative(self) -> bool:
        return self.is_positive

    @abstractmethod
    def on_damage_event(self):
        pass

    @abstractmethod
    def on_move_events(self):
        pass

    @abstractmethod
    def on_shoot_events(self):
        pass

    @abstractmethod
    def on_death_events(self):
        pass

    @abstractmethod
    def on_mech_kill_events(self):
        pass

    @abstractmethod
    def on_npc_kill_events(self):
        pass

    @abstractmethod
    def on_undefined_actions_events(self):
        pass