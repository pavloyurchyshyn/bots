from typing import List
from pygame import Surface, Rect
from pygame.draw import rect as draw_rect
from global_obj.main import Global
from core.player.player import Player
from visual.cards.skill.card import SkillCard
from game_client.game_match.stages.match_menu.settings.windows_sizes import CardsDeck


class CardsC:
    CARDS_MOVE_SPEED = 250
    player: Player

    def __init__(self):
        self.deck_back_surface = Surface((CardsDeck.h_size, CardsDeck.v_size))
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

    def draw_cards(self):
        Global.display.blit(self.deck_back_surface, (CardsDeck.x, CardsDeck.y + self.cards_dy))

    def collect_skills_deck(self):
        self.skills_deck.clear()
        if self.player.mech:
            for skill in self.player.skills:
                self.skills_deck.append(SkillCard(skill))
            print(self.player.skills)
            print(self.skills_deck)
            # print('mech', self.player.mech)
            # print('details', self.player.mech.get_details())
            # print('AAAAA', self.player.mech.skills)
        #     # Global.skill_cards_fabric.get_cards_for_skill()

    def get_rect(self) -> Rect:
        return Rect(CardsDeck.x, CardsDeck.y + self.cards_dy, CardsDeck.h_size, CardsDeck.v_size)