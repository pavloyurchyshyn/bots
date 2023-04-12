from global_obj.main import Global
from core.mech.skills.skill import BaseSkill
from core.mech.skills.constants import SkillAttrs


class SkillSerializer:

    @staticmethod
    def json_to_skill(json_: dict) -> BaseSkill:
        s = Global.skill_pool.get_skill_by_id(json_[SkillAttrs.UID])
        s.cooldown = json_.get(SkillAttrs.CD, s.cooldown)
        s.energy_cost = json_.get(SkillAttrs.ECost, s.energy_cost)
        # s.use_dict = json_.get(SkillAttrs.UseJson, s.use_dict)
        return s

    @staticmethod
    def skill_to_json(skill: BaseSkill) -> dict:
        return {
            SkillAttrs.UID: skill.unique_id,
            SkillAttrs.CD: skill.cooldown,
            SkillAttrs.ECost: skill.energy_cost,
            # SkillAttrs.UseJson: skill.use_dict,
        }

    @staticmethod
    def skill_to_json_by_id(uid: str) -> dict:
        return SkillSerializer.skill_to_json(Global.skill_pool.get_skill_by_id(uid))
