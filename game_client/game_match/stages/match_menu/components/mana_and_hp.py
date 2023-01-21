from global_obj.main import Global
from pygame.draw import rect as draw_rect
from game_client.game_match.stages.match_menu.settings.windows_sizes import HPBar, ManaBar


class ManaAndHpC:

    def draw_mana_hp(self):
        draw_rect(Global.display, (255, 255, 255), HPBar.rect, 3)
        draw_rect(Global.display, (255, 255, 255), ManaBar.rect, 3)
