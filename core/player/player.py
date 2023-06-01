from typing import Dict, Optional, List
from global_obj.main import Global
from core.mech.mech import BaseMech
from core.mech.skills.skill import BaseSkill
from core.player.abs import PlayerAbs
from core.player.scenario import Scenario
from core.player.constants import PlayerAttrs


class PlayerObj(PlayerAbs):
    """Internal player object"""
    def __init__(self,
                 nickname,
                 spawn: tuple[int, int],
                 scenario: Dict[int, dict] = None,
                 mech: BaseMech = None,
                 ready: bool = False,
                 under_bot_control: bool = False,
                 ):
        self.ready: bool = ready
        self.nickname: str = nickname
        self.spawn: tuple[int, int] = tuple(spawn)
        self.mech: BaseMech = mech
        self.under_bot_control: bool = under_bot_control
        self.scenario: Scenario = Scenario(self, scenario=scenario)

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
        if PlayerAttrs.Mech in d and d[PlayerAttrs.Mech]:
            Global.logger.info(f'Received mech dict: {d[PlayerAttrs.Mech]}')
            mech = Global.mech_serializer.dict_to_mech(d.pop(PlayerAttrs.Mech))
        else:
            d.pop(PlayerAttrs.Mech, None)
            mech = None
        return PlayerObj(**d, mech=mech)

    def update_attrs(self, attrs_dict: dict):
        # self.mech.set_attrs(attrs_dict.pop(PlayerAttrs.Mech, {}))
        # TODO set vanile_details
        for attr, val in attrs_dict.items():
            setattr(self, attr, val)

    @property
    def skills(self) -> List[BaseSkill]:
        if self.mech:
            return self.mech.skills.copy()
        else:
            return []

    @property
    def latest_scenario_mech(self) -> Optional[BaseMech]:
        for action in reversed(self.scenario.actions.values()):
            if action and action.mech_copy:
                return action.mech_copy

        return self.mech.get_copy()

    @property
    def latest_scenario_skills(self) -> List[BaseSkill]:
        for action in reversed(self.scenario.actions.values()):
            if action and action.mech_copy:
                return action.mech_copy.skills

        return self.mech.get_copy().skills

    def get_latest_scenario_skill(self, skill_uid: str):
        for skill in self.latest_scenario_skills:
            if skill.unique_id == skill_uid:
                return skill

    @property
    def first_empty_action_slot(self) -> int:
        for k, action in reversed(self.scenario.actions.items()):
            if action is None:
                return k