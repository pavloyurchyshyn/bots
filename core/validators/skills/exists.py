from global_obj.main import Global
from core.validators.base import BaseValidator
from core.mech.base.skills.skill import BaseSkill


class SkillDoesntExistError(Exception):
    pass


class SkillExistsV(BaseValidator):
    error = SkillDoesntExistError

    @staticmethod
    def validate(skill: BaseSkill, *args, **kwargs):
        return skill in Global.skill_pool.skills


class SkillUIDExistsV(BaseValidator):
    error = SkillDoesntExistError

    @staticmethod
    def validate(skill_uid: str, *args, **kwargs):
        return skill_uid in Global.skill_pool.id_to_skill
