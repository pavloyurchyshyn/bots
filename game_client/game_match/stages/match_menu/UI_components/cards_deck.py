from typing import List
from pygame import Surface, Rect
from pygame.draw import rect as draw_rect
from global_obj.main import Global
from core.player.player import Player
from visual.cards.skill.card import SkillCard
from game_client.game_match.stages.match_menu.settings.windows_sizes import CardsDeck
from settings.visual.cards import SkillCardSize
from visual.cards.skill.skill_cards_fabric import SkillsCardsFabric


class CardsC:
    CARDS_MOVE_SPEED = 250
    player: Player
    selected_card_to_use: SkillCard
    skill_cards_fabric: SkillsCardsFabric

    def __init__(self):
        self.deck_back_surface = Surface(CardsDeck.size)
        self.deck_back_surface.fill((80, 150, 80))
        draw_rect(self.deck_back_surface, (255, 255, 255), (0, 0, CardsDeck.h_size, CardsDeck.v_size), 1)
        self.skills_deck: List[SkillCard] = []
        self.cards_dy = 0

    def deck_cards_move_check(self):
        if CardsDeck.y + self.cards_dy > Global.display.get_height() - CardsDeck.v_size:
            self.cards_dy -= Global.clock.d_time * self.CARDS_MOVE_SPEED
            if CardsDeck.y + self.cards_dy < Global.display.get_height() - CardsDeck.v_size:
                self.cards_dy = Global.display.get_height() - CardsDeck.v_size - CardsDeck.y

    def cards_deck_collide_point(self, pos: tuple) -> bool:
        return self.get_rect().collidepoint(*pos)

    def draw_cards(self, dx=0, dy=0):
        Global.display.blit(self.deck_back_surface, (CardsDeck.x, CardsDeck.y + self.cards_dy))
        top_card = None
        for skill_card in self.skills_deck:
            if skill_card == self.selected_card_to_use:
                pass
            elif self.get_rect().collidepoint(Global.mouse.pos) and skill_card.get_rect(dx, dy).collidepoint(
                    Global.mouse.pos):
                top_card = skill_card
            else:
                skill_card.draw(dx, dy)
        if top_card:
            top_card.draw(dx, dy - top_card.v_size * 0.1)
            draw_rect(Global.display,
                      (255, 255, 255),
                      top_card.get_rect(dx, dy - top_card.v_size * 0.1),
                      width=3,
                      border_radius=top_card.style.border_radius)
        if self.selected_card_to_use:
            self.selected_card_to_use.draw(dx, dy - self.selected_card_to_use.v_size * 0.1)
            draw_rect(Global.display,
                      (0, 255, 0),
                      self.selected_card_to_use.get_rect(dx, dy - self.selected_card_to_use.v_size * 0.1),
                      width=5,
                      border_radius=self.selected_card_to_use.style.border_radius)

    def collect_skills_deck(self):
        self.skills_deck.clear()
        if self.player.mech:
            for skill in self.player.skills:
                self.skills_deck.append(self.skill_cards_fabric.get_cards_for_skill(skill))  # TODO move to factory

            self.calculate_cards_positions()

    def calculate_cards_positions(self):
        # place for cards with step from borders
        w_space = CardsDeck.h_size
        cards_num = len(self.skills_deck)
        # size for all cards
        sum_width = cards_num * SkillCardSize.X_SIZE
        step_between_cards = 0
        size_scale = 1

        if w_space > sum_width:
            step_between_cards = 2
        else:
            size_scale = (w_space - SkillCardSize.X_SIZE // 2) / sum_width

        step_w = (cards_num - 1) * step_between_cards
        x = CardsDeck.x + CardsDeck.h_size // 2 - step_w - sum_width // 2 * size_scale

        for card in sorted(self.skills_deck, key=lambda c: c.x):
            card.x = x
            card.y = CardsDeck.y + (CardsDeck.v_size - card.v_size) // 2
            x += SkillCardSize.X_SIZE * size_scale + step_between_cards

    def get_rect(self) -> Rect:
        return Rect(CardsDeck.x, CardsDeck.y + self.cards_dy, CardsDeck.h_size, CardsDeck.v_size)
