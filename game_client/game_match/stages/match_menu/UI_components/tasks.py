from global_obj.main import Global
from pygame.draw import rect as draw_rect
from game_client.game_match.stages.match_menu.settings.windows_sizes import Tasks
from visual.UI.base.text import Text


class TasksC:
    def __init__(self):
        self.task_window_title = Text('tasks_title', text="Tasks",
                                      from_left=True,
                                      x_k=Tasks.Title.x,
                                      y_k=Tasks.Title.y,
                                      v_size_k=Tasks.Title.v_size,
                                      h_size_k=Tasks.Title.h_size,
                                      )
        self.task_window_title.style.surface_color = (50, 50, 50)
        self.task_window_title.render()

    def draw_tasks(self):
        draw_rect(Global.display, (255, 255, 255), Tasks.rect, 1)
        self.task_window_title.draw()
