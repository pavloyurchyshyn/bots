from global_obj.main import Global
from core.mech.base.mech import BaseMech
from core.player.abs import PlayerAbs
from core.player.scenario import Scenario
from core.player.constants import PlayerAttrs


class PlayerObj(PlayerAbs):
    def __init__(self,
                 nickname,
                 spawn: tuple[int, int],
                 actions_count: int = 3,
                 mech: BaseMech = None,
                 ready: bool = False,
                 ):
        self.ready: bool = ready
        self.nickname: str = nickname
        self.spawn: tuple[int, int] = spawn
        self.mech: BaseMech = mech
        self.scenario: Scenario = Scenario(self, actions_count=actions_count)

    def get_dict(self):
        return {
            PlayerAttrs.Ready: self.ready,
            PlayerAttrs.Nickname: self.nickname,
            PlayerAttrs.Spawn: self.spawn,
            PlayerAttrs.Mech: Global.mech_serializer.mech_to_dict(self.mech) if self.mech else None,
            PlayerAttrs.Scenario: self.scenario.get_dict(),
        }

    @staticmethod
    def get_player_from_dict(d: dict) -> 'PlayerObj':
        if PlayerAttrs.Mech in d:
            Global.logger.info(f'Received mech dict: {d[PlayerAttrs.Mech]}')
            mech = Global.mech_serializer.dict_to_mech(d.pop(PlayerAttrs.Mech))
        else:
            mech = None
        scenario = d.pop(PlayerAttrs.Scenario, {})
        return PlayerObj(**d, actions_count=scenario.get('actions_count'), mech=mech)

    def update_attrs(self, attrs_dict: dict):
        # self.mech.set_attrs(attrs_dict.pop(PlayerAttrs.Mech, {}))
        # TODO set details
        for attr, val in attrs_dict.items():
            setattr(self, attr, val)

    @property
    def skills(self) -> list:
        if self.mech:
            return self.mech.skills.copy()
        else:
            return []
