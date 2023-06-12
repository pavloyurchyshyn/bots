from typing import List
from global_obj.logger import get_logger
from core.mech.skills.skill import BaseSkill

LOGGER = get_logger()


class SkillsPool:
    def __init__(self):
        self.skills: List[BaseSkill] = []
        self.id_to_skill: dict = {}

    def get_skill_by_id(self, unique_id) -> BaseSkill:
        return self.id_to_skill.get(unique_id)

    def add_skill(self, skill: BaseSkill):
        """
        :param skill: already initialized object
        """
        self.id_to_skill[skill.unique_id] = skill
        self.skills.append(skill)
        LOGGER.debug(f'Added skill to skill pool: {skill.__dict__}')  # \n {self.id_to_skill}')

    def del_skill_by_id(self, unique_id):
        skill = self.id_to_skill.pop(unique_id, None)
        if skill is not None:
            self.skills.remove(skill)
