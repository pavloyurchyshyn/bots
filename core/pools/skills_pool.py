import inspect
from typing import List, Dict, Type
from global_obj.logger import get_logger
from core.mech.skills.skill import BaseSkill
from core import vanilla_skills as skills_module

LOGGER = get_logger()


class SkillsPool:
    def __init__(self):
        self.skills: List[BaseSkill] = []
        self.id_to_skill: dict = {}
        self.classes_dict: Dict[str, Type] = {}
        self.collect_skills_classes()

    def get_class_by_name(self, name: str):
        return self.classes_dict.get(name)

    def collect_skills_classes(self):
        self.classes_dict.clear()
        for _, skill_class in inspect.getmembers(skills_module, inspect.isclass):
            self.classes_dict[skill_class.name] = skill_class

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
