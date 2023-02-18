from visual.cards.skill import SkillCard
from core.mech.base.skills.skill import BaseSkill
from core.mech.base.pools.skills_pool import SkillsPool


class SkillsCardsFabric:
    def __init__(self, skill_pool: SkillsPool):
        self.skill_pool: SkillsPool = skill_pool
        self.cards = {}

    def create_card(self, skill_uid: str, x: int = 0, y: int = 0) -> SkillCard:
        skill: BaseSkill = self.skill_pool.get_skill_by_id(skill_uid)
        card = SkillCard(uid=skill_uid, skill=skill, x=x, y=y)
        self.add_card(card)
        return card

    def get_card(self, skill_uid: str) -> SkillCard:
        if skill_uid in self.cards:
            return self.cards[skill_uid]
        else:
            return self.create_card(skill_uid)

    def get_cards_for_skill(self, skill: BaseSkill, x: int = 0, y: int = 0) -> SkillCard:
        if skill.unique_id not in self.cards:
            self.add_card(SkillCard(skill.unique_id, skill, x, y))

        return self.cards[skill.unique_id]

    def add_card(self, skill_cards: SkillCard):
        self.cards[skill_cards.uid] = skill_cards

    def clean(self):
        self.cards.clear()
