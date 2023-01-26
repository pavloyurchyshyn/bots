from global_obj.main import Global
from pygame.draw import rect as draw_rect
from game_client.game_match.stages.match_menu.settings.windows_sizes import MechWin


class MechC:

    def draw_mech_win(self):
        draw_rect(Global.display, (255, 255, 255), MechWin.rect, 1)
