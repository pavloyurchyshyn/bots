from global_obj.main import Global
from visual.cards.skill.card import SkillCard
from pygame.draw import rect as draw_rect, line as draw_line, circle as draw_circle
from core.mech.base.skills.constants import Targets


class CardUseC:
    def __init__(self):
        self.selected_card_to_use: SkillCard = None

    def draw_use_trace(self):
        if self.selected_card_to_use:
            m_pos = Global.mouse.pos
            color = (50, 255, 50)
            if self.w.window_rect.collidepoint(m_pos):
                m_pos = self.w.get_normalized_mouse_pos()
                if not self.selected_card_to_use.skill.is_valid_target(Targets.Tile):
                    color = (255, 50, 50)

            draw_line(Global.display, (100, 255, 255),
                      self.selected_card_to_use.get_center(dy=self.cards_dy),
                      m_pos,
                      4
                      )
            draw_circle(Global.display, color, m_pos, 5)
