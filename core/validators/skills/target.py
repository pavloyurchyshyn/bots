from core.validators.base import BaseValidator
from core.mech.base.skills.skill import BaseSkill


class BadTargetTypeError(Exception):
    pass


class TargetV(BaseValidator):
    error = BadTargetTypeError

    @staticmethod
    def validate(skill: BaseSkill, target: str, *args, **kwargs) -> bool:
        return target in skill.targets
