from launch import GameRunner
from global_obj import Global
from visual.UI.base.button import Button
from visual.UI.base.style import ButtonStyle


class Body:
    def __init__(self):
        self.buttons = []
        for i in range(0, 10):
            self.buttons.append(
                Button(f'button_{i}', 'AHAHHAH',
                       on_click_action=lambda button: print(f'Hello from {button.uid}!'),
                       x_k=0.1 * i, y_k=0.1 * i,
                       h_size_k=0.1,
                       v_size_k=0.05,
                       style=ButtonStyle(
                           from_left=False, from_bot=False, from_top=False,
                           surface_color=(10 * i, 10, 10 * i),
                       ),
                       )
            )

        self.buttons.append(Button(f'button_{999}', 'AHAHHAH',
                                   on_click_action=lambda button: print(f'Hello from {button.uid}!'),
                                   x_k=0.3, y_k=0.5,
                                   h_size_k=0.1,
                                   v_size_k=0.05,
                                   from_left=False, from_bot=False, from_top=False,
                                   surface_color=(10, 10, 10),
                                   ))

    def game_loop(self):
        for b in self.buttons:
            b.draw()
            if Global.mouse.l_up and b.collide_point(Global.mouse.pos):
                b.do_action()


if __name__ == '__main__':
    GameRunner(Body()).run()
