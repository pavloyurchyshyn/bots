from pygame import Surface, Rect
from pygame.draw import rect as draw_rect

from visual.UI.base.text import Text
from visual.UI.utils import get_surface
from visual.UI.constants.colors import CommonColors
from visual.cards.skill.style import SkillCardStyle
from visual.cards.skill.card_abs import SkillCardAbs

from settings.visual.cards import SkillCardSize

from core.mech.base.skills.skill import BaseSkill


class SkillCard(SkillCardAbs):
    Colors = CommonColors
    default_style = SkillCardStyle()

    def __init__(self, uid: str,
                 skill: BaseSkill,
                 x: int = 0, y: int = 0,
                 h_size: int = SkillCardSize.X_SIZE,
                 v_size: int = SkillCardSize.Y_SIZE,
                 style=None):
        self.uid: str = uid
        self.x: int = x
        self.y: int = y
        self.h_size: int = h_size
        self.v_size: int = v_size

        self.style = style if style else self.default_style

        self.skill = skill
        self.surface: Surface = get_surface(self.h_size, self.v_size, color=(50, 50, 50))
        self.text: Text = Text(uid='',
                               text=skill.verbal_name,  # TODO add localization
                               y_k=0.01,
                               v_size_k=0.2,
                               h_size_k=0.98,
                               parent_surface=self.surface, auto_draw=False)

        self.render()

    def render(self):
        self.surface.fill((0, 0, 0, 0))
        self.draw_back()
        self.text.draw()
        self.draw_rect()

    def draw_rect(self):
        draw_rect(self.surface, self.style.border_color, (0, 0, self.h_size, self.v_size), 1, self.style.border_radius)

    def draw_back(self):
        draw_rect(self.surface, self.style.border_color, (0, 0, self.h_size, self.v_size), 0, self.style.border_radius)

    def get_rect(self, dx: int = 0, dy: int = 0) -> Rect:
        return Rect(self.x + dx, self.y + dy, self.h_size, self.v_size)
