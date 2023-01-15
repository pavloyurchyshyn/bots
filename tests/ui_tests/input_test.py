from launch import GameRunner
from visual.UI.base.input import InputBase
from visual.UI.constants.attrs import Attrs
from global_obj.main import Global

text_data = {
    Attrs.HSizeK: 0.5,
    Attrs.VSizeK: 0.5,
}


class Body:
    def __init__(self):
        self.input = InputBase('test',
                               text='here',
                               # x_k=0.35,
                               # y_k=0.45,
                               default_text='Enter text:',
                               h_size_k=0.05,
                               v_size_k=0.1,
                               surface_color=(100, 100, 100),
                               text_kwargs=text_data,
                               )

    def game_loop(self):
        Global.display.fill((0, 0, 0))
        if Global.mouse.l_up and self.input.collide_point(Global.mouse.pos):
            self.input.focus()
        self.input.update()
        self.input.draw()


if __name__ == '__main__':
    GameRunner(Body()).run()
