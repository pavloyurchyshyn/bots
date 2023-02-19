from abc import abstractmethod
from core.mech.base.mech import BaseMech


class PlayerAbs:
    is_admin: bool
    is_admin: bool
    token: str
    ready: bool
    nickname: str
    spawn: tuple[int, int]
    mech: BaseMech

    @abstractmethod
    def get_dict(self) -> dict:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_player_from_dict(d: dict) -> 'Player':
        raise NotImplementedError

    @abstractmethod
    def update_attrs(self, attrs_dict: dict):
        raise NotImplementedError
