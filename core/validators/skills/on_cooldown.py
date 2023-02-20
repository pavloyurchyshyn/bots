from core.validators.base import BaseValidator
from core.mech.base.skills.skill import BaseSkill


class OnCooldownError(Exception):
    pass


class OnCooldownV(BaseValidator):
    error = OnCooldownError

    @staticmethod
    def validate(skill: BaseSkill, *args, **kwargs) -> bool:
        return skill.on_cooldown
