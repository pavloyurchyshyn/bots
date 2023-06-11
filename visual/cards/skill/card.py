from pygame import Surface, Rect
from pygame.draw import rect as draw_rect, line as draw_line

from visual.UI.base.text import Text
from visual.UI.utils import get_surface
from visual.UI.constants.colors import CommonColors
from visual.cards.skill.style import SkillCardStyle
from visual.cards.skill.card_abs import SkillCardAbs

from settings.visual.cards import SkillCardSize

from core.mech.skills.skill import BaseSkill

from global_obj.main import Global


class SkillCard(SkillCardAbs):
    Colors = CommonColors
    default_style = SkillCardStyle()

    # TODO separate skill and visual
    def __init__(self,
                 skill: BaseSkill,
                 uid: str = None,
                 x: int = 0, y: int = 0,
                 h_size: int = SkillCardSize.X_SIZE,
                 v_size: int = SkillCardSize.Y_SIZE,
                 style=None):
        self.uid: str = f'{skill.unique_id}_card' if uid is None else uid
        self.x: int = x
        self.y: int = y
        self.h_size: int = h_size
        self.v_size: int = v_size

        self.style = style if style else self.default_style

        self.skill: BaseSkill = skill
        self.surface: Surface = get_surface(self.h_size, self.v_size, transparent=1)
        self.text: Text = Text(uid='',
                               text=skill.verbal_name,  # TODO add localization
                               y_k=0.01,
                               v_size_k=0.2,
                               h_size_k=0.98,
                               parent_surface=self.surface, auto_draw=False)

        self.mute_surface: Surface = self.get_mute_surface(self.style.on_cd_background_color)# TODO move to textures cache
        self.invalid_surface: Surface = self.get_mute_surface(self.style.invalid_background_color) # TODO move to textures cache

        self.render()

    def render(self):
        self.surface.fill((0, 0, 0, 0))
        self.draw_back()
        self.text.draw()
        self.draw_border()

    def draw_border(self):
        draw_rect(self.surface, self.style.border_color, (0, 0, self.h_size, self.v_size), 1, self.style.border_radius)

    def draw_back(self):
        draw_rect(self.surface, self.style.back_color, (0, 0, self.h_size, self.v_size), 0, self.style.border_radius)

    def get_rect(self, dx: int = 0, dy: int = 0) -> Rect:
        return Rect(self.x + dx, self.y + dy, self.h_size, self.v_size)

    def get_center(self, dx: int = 0, dy: int = 0) -> tuple:
        return self.x + dx + self.h_size // 2, self.y + dy + self.v_size // 2

    def draw(self, dx=0, dy=0):
        Global.display.blit(self.surface, (self.x + dx, self.y + dy))

        if self.skill.on_cooldown:
            Global.display.blit(self.mute_surface, (self.x + dx, self.y + dy))

    def get_mute_surface(self, color) -> Surface:
        card_surf = get_surface(h_size=self.h_size,
                                v_size=self.v_size,
                                transparent=1,
                                )
        draw_rect(card_surf,
                  color,
                  (0, 0, self.h_size, self.v_size),
                  0,
                  self.style.border_radius)
        return card_surf
