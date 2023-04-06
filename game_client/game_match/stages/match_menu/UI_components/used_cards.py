from typing import Dict
from pygame import Surface, Rect
from global_obj.main import Global
from pygame.draw import rect as draw_rect
from game_client.game_match.stages.match_menu.settings.windows_sizes import UsedCards, HpBar
from settings.visual.cards import SkillCardSize
from visual.cards.skill.card import SkillCard

from core.player.player import PlayerObj


class UsedCardsC:
    player: PlayerObj
    cards_dy: int
    CARDS_MOVE_SPEED: int

    def __init__(self):
        self.used_cards_back_surface = None
        self.used_cards_positions_dict: Dict[int, tuple] = {}
        self.used_cards_dict: Dict[int, SkillCard] = {}
        self.__render()

    def __render(self):
        self.used_cards_back_surface = Surface(UsedCards.size)
        self.used_cards_back_surface.fill((100, 100, 100))

        self.__render_used_cards_rects()

        draw_rect(self.used_cards_back_surface, (255, 255, 255), (0, 0, UsedCards.h_size, UsedCards.v_size), 1)

    def __render_used_cards_rects(self) -> list:
        rects = []
        actions_num = self.processor.settings.actions_count
        free_size = UsedCards.h_size - actions_num * SkillCardSize.X_SIZE
        step = free_size / (actions_num + 1)
        x = 0 if free_size < 0 else step

        y = (UsedCards.v_size - SkillCardSize.Y_SIZE) // 2

        for i in range(actions_num):
            draw_rect(self.used_cards_back_surface,
                      (255, 255, 255),
                      (x, y, SkillCardSize.X_SIZE, SkillCardSize.Y_SIZE),
                      1,
                      SkillCard.default_style.border_radius)

            self.used_cards_positions_dict[i] = (x, y)
            self.used_cards_dict[i] = None

            x += step
            x += SkillCardSize.X_SIZE

        return rects

    def draw_used_cards(self):
        Global.display.blit(self.used_cards_back_surface, (UsedCards.x, UsedCards.y))
        # for i, pos in self.ca

    def used_cards_move_check(self):
        if HpBar.y + self.cards_dy < UsedCards.y + UsedCards.v_size:
            self.cards_dy += Global.clock.d_time * self.CARDS_MOVE_SPEED
            if HpBar.y + self.cards_dy > UsedCards.y + UsedCards.v_size:
                self.cards_dy = UsedCards.y + UsedCards.v_size - HpBar.y

    def used_cards_collide_point(self, pos: tuple) -> bool:
        return Rect(UsedCards.x, UsedCards.y, UsedCards.h_size, UsedCards.v_size).collidepoint(*pos)

    def use_card(self, uid: str):
        # TODO
        pass