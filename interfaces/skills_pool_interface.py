from typing import List, Dict, Union
from core.mech.skills.skill import BaseSkill


class SkillsPoolInterface:
    skills: List[BaseSkill]
    id_to_skill: Dict[Union[str, int], BaseSkill]

    def get_skill_by_id(self, unique_id) -> BaseSkill:
        pass

    def add_skill(self, skill: BaseSkill):
        pass

    def del_skill_by_id(self, unique_id):
        pass
