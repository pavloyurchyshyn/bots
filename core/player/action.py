from typing import List
from core.mech.mech import BaseMech
from core.mech.skills.skill import BaseSkill
from core.mech.skills.constants import Targets

class Action:
    """
    One skill use
    """
    def __init__(self, skill_uid:str, use_attrs: dict, mech_copy: BaseMech):
        self.skill_uid = skill_uid
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
    def mech_skills(self) -> List[BaseSkill]:
        return self.mech_copy.skills

    @property
    def mech_details(self):
        return self.mech_copy.details