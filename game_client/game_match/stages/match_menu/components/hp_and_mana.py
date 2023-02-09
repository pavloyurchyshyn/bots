from global_obj.main import Global
from pygame.draw import rect as draw_rect
from game_client.game_match.stages.match_menu.settings.windows_sizes import HpBar, ManaBar


class HpAndManaC:

    def draw_hp_and_mana_win(self):
        draw_rect(Global.display, (55, 255, 55), (HpBar.x, HpBar.y + self.cards_dy, HpBar.h_size, HpBar.v_size), 3)
        draw_rect(Global.display, (55, 55, 255), (ManaBar.x, ManaBar.y + self.cards_dy, ManaBar.h_size, ManaBar.v_size), 3)
