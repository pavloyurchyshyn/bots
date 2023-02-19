from abc import abstractmethod
from core.mech.base.skills.skill import BaseSkill
from visual.cards.skill.style import SkillCardStyle


class SkillCardAbs:
    uid: str
    x: int
    y: int
    h_size: int
    v_size: int
    style: SkillCardStyle
    skill: BaseSkill

    @abstractmethod
    def render(self):
        raise NotImplementedError

    @abstractmethod
    def draw_rect(self):
        raise NotImplementedError

    @abstractmethod
    def draw_back(self):
        raise NotImplementedError
