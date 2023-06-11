from global_obj.main import Global
from typing import List
from types import MappingProxyType
from core.mech.mech import BaseMech
from core.mech.skills.skill import BaseSkill
from core.mech.details.detail import BaseDetail
from core.mech.skills.constants import Targets

class Action:
    """
    One skill use
    """
    _skip: bool = False
    def __init__(self, slot: int, skill_uid:str, use_attrs: dict, mech_copy: BaseMech, valid: bool = True):
        self.slot = slot
        self.skill_uid = skill_uid
        self.use_attrs: MappingProxyType = MappingProxyType(use_attrs)
        self.mech_copy: BaseMech = mech_copy
        self.valid: bool = valid

    def set_use_dict(self, use_attrs: dict):
        self.use_attrs = use_attrs

    def set_mech_copy(self, mech_copy):
        self.mech_copy = mech_copy

    @property
    def target_xy(self) -> tuple:
        return tuple(self.use_attrs.get(Targets.Tile))
    @property
    def mech_skills(self) -> List[BaseSkill]:
        return self.mech_copy.skills

    @property
    def mech_details(self) -> List[BaseDetail]:
        return self.mech_copy.details

    def get_dict(self) -> dict:
        # TODO move to constants ?
        return {'valid': self.valid,
                'mech_copy': Global.mech_serializer.mech_to_dict(self.mech_copy),
                'skill_uid': self.skill_uid,
                'use_attrs': dict(self.use_attrs),
                'skip': self._skip,
                }

    @property
    def skill(self) -> BaseSkill:
        skill = tuple(filter(lambda s: s.unique_id == self.skill_uid, self.mech_skills))

        assert len(skill) <= 1  # TODO check it later

        return skill[0] if skill else None

    @property
    def skip(self):
        return self._skip

    def make_valid(self):
        self.valid = True

    def make_invalid(self):
        self.valid = False


class SkipAction(Action):
    _skip = True
    def __init__(self, slot, mech_copy: BaseMech, *_, **__):
        super().__init__(slot=slot, use_attrs={}, mech_copy=mech_copy, skill_uid=None)