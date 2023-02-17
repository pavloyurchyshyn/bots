from global_obj.main import Global
from core.player.abs import PlayerAbs
from core.mech.base.mech import BaseMech
from core.player.constants import PlayerAttrs


class Player(PlayerAbs):
    def __init__(self, token,
                 nickname,
                 spawn: tuple[int, int],
                 # number,
                 # actions_count,
                 mech: BaseMech = None,
                 # addr=None,
                 is_admin: bool = False,
                 ready: bool = False,
                 ):
        self.is_admin: bool = is_admin
        self.token: str = token
        self.ready: bool = ready
        self.nickname: str = nickname
        self.spawn: tuple[int, int] = spawn
        self.mech: BaseMech = mech

    def get_dict(self):
        return {
            PlayerAttrs.Token: self.token,
            PlayerAttrs.IsAdmin: self.is_admin,
            PlayerAttrs.Ready: self.ready,
            PlayerAttrs.Nickname: self.nickname,
            PlayerAttrs.Spawn: self.spawn,
            PlayerAttrs.Mech: Global.mech_serializer.mech_to_dict(self.mech) if self.mech else None,
        }

    @staticmethod
    def get_player_from_dict(d: dict) -> 'Player':
        if PlayerAttrs.Mech in d:
            mech = Global.mech_serializer.dict_to_mech(d.pop(PlayerAttrs.Mech))
        else:
            mech = None
        return Player(**d, mech=mech)
