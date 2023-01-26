from global_obj.main import Global
from pygame.draw import rect as draw_rect
from game_client.game_match.stages.match_menu.settings.windows_sizes import Tasks


class TasksC:
    def draw_tasks(self):
        draw_rect(Global.display, (255, 255, 255), Tasks.rect, 1)
