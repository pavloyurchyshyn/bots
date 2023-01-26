from global_obj.main import Global
from pygame.draw import rect as draw_rect
from game_client.game_match.stages.match_menu.settings.windows_sizes import UsedCards, CardsDeck


class UsedCardsC:

    def draw_used_cards(self):
        draw_rect(Global.display, (255, 255, 255), UsedCards.rect, 1)
