from global_obj.main import Global
from core.validators.base import BaseValidator
from core.mech.base.skills.skill import BaseSkill


class BadUseError(Exception):
    pass


class UseDictV(BaseValidator):
    error = BadUseError

    @staticmethod
    def validate(skill: BaseSkill, *args, **kwargs) -> bool:
        use = skill.use_dict
