from core.mech.skills.abs import BaseSkillInterface
from core.entities.entity import BaseEntity


class Damage:
    def __init__(self, dealer: BaseEntity, target: BaseEntity, skill: BaseSkillInterface):
        self.dealer: BaseEntity = dealer
        self.target: BaseEntity = target
        self.skill: BaseSkillInterface = skill