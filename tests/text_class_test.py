from launch import GameRunner
from visual.UI.base.text import Text
from settings.base import ROOT_OF_GAME


class Body:
    def __init__(self):
        self.texts = []
        for i in range(1, 11):
            self.texts.append(
                Text('test_text', 'AHAHHAH',
                     x_k=i / 10, y_k=i / 10,
                     from_left=False, from_bot=False, from_top=False,
                     color=(20 * i, 155, 20 * i),
                     surface_color=(255 / i, 255 / i, 255 / i)
                     )
            )

    def game_loop(self):
        for t in self.texts:
            t.draw()


if __name__ == '__main__':
    GameRunner(Body()).run()
