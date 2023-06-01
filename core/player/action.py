from typing import List
from core.mech.mech import BaseMech
from core.mech.skills.skill import BaseSkill
from server_stuff.constants.requests import GameStgConst as GSC
from core.mech.skills.constants import Targets

class Action:
    """
    One skill use
    """
    def __init__(self, use_attrs: dict, mech_copy: BaseMech):
        self.use_attrs: dict = use_attrs
        self.mech_copy: BaseMech = mech_copy

    def set_use_dict(self, use_attrs: dict):
        self.use_attrs = use_attrs

    def set_mech_copy(self, mech_copy):
        self.mech_copy = mech_copy

    @property
    def target_xy(self) -> tuple:
        return self.use_attrs.get(Targets.Tile)
    @property
    def skills(self) -> List[BaseSkill]:
        return self.mech_copy.skills

    @property
    def details(self):
        return self.mech_copy.details