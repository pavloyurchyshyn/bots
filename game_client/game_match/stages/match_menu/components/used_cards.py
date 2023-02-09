from pygame import Surface, Rect
from global_obj.main import Global
from pygame.draw import rect as draw_rect
from game_client.game_match.stages.match_menu.settings.windows_sizes import UsedCards, HpBar


class UsedCardsC:
    def __init__(self):
        self.used_cards_back_surface = Surface((UsedCards.h_size, UsedCards.v_size))
        self.used_cards_back_surface.fill((100, 100, 100))
        draw_rect(self.used_cards_back_surface, (255, 255, 255), (0, 0, UsedCards.h_size, UsedCards.v_size), 1)

    def draw_used_cards(self):
        Global.display.blit(self.used_cards_back_surface, (UsedCards.x, UsedCards.y))

    def used_cards_move_check(self):
        if HpBar.y + self.cards_dy < UsedCards.y + UsedCards.v_size:
            self.cards_dy += Global.clock.d_time * self.CARDS_MOVE_SPEED
            if HpBar.y + self.cards_dy > UsedCards.y + UsedCards.v_size:
                self.cards_dy = UsedCards.y + UsedCards.v_size - HpBar.y

    def used_cards_collide_point(self, pos: tuple) -> bool:
        return Rect(UsedCards.x, UsedCards.y, UsedCards.h_size, UsedCards.v_size).collidepoint(*pos)
