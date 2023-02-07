from visual.cards.base import Card
from visual.UI.utils import get_surface
from visual.UI.base.text import Text
from settings.visual.cards import SkillCardSize
from visual.UI.base.style import Style
from core.mech.base.skills.skill import BaseSkill


class SkillCard(Card):
    def __init__(self, uid: str,
                 skill: BaseSkill,
                 x, y,
                 style: Style = None,
                 size_x=SkillCardSize.X_SIZE, size_y=SkillCardSize.Y_SIZE):
        super().__init__(uid, x, y, style=style, size_x=size_x, size_y=size_y)
        self.skill: BaseSkill = skill
        self.surface = get_surface(self.size_x, self.size_y, color=(50, 50, 50))
        self.text: Text = Text(uid='',
                               text=skill.verbal_name,  # TODO add localization
                               y_k=0.01,
                               v_size_k=0.2,
                               h_size_k=0.98,
                               parent_surface=self.surface, auto_draw=False)
        self.render()

    def render(self):
        self.fill_surface_due_to_border_attrs(self.surface, (50, 50, 50))
        self.text.draw()
        self.draw_border(self.surface)