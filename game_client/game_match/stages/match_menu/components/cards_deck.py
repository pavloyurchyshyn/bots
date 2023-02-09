from pygame import Surface, Rect
from global_obj.main import Global
from pygame.draw import rect as draw_rect
from game_client.game_match.stages.match_menu.settings.windows_sizes import CardsDeck


class CardsC:
    CARDS_MOVE_SPEED = 250

    def __init__(self):
        self.deck_back_surface = Surface((CardsDeck.h_size, CardsDeck.v_size))
        self.deck_back_surface.fill((80, 150, 80))
        draw_rect(self.deck_back_surface, (255, 255, 255), (0, 0, CardsDeck.h_size, CardsDeck.v_size), 1)

        self.cards_dy = 0

    def deck_cards_move_check(self):
        if CardsDeck.y + self.cards_dy > Global.display.get_height() - CardsDeck.v_size:
            self.cards_dy -= Global.clock.d_time * self.CARDS_MOVE_SPEED
            if CardsDeck.y + self.cards_dy < Global.display.get_height() - CardsDeck.v_size:
                self.cards_dy = Global.display.get_height() - CardsDeck.v_size - CardsDeck.y

    def cards_deck_collide_point(self, pos: tuple) -> bool:
        return Rect(CardsDeck.x, CardsDeck.y + self.cards_dy, CardsDeck.h_size, CardsDeck.v_size).collidepoint(*pos)

    def draw_cards(self):
        Global.display.blit(self.deck_back_surface, (CardsDeck.x, CardsDeck.y + self.cards_dy))
