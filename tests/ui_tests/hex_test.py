from launch import GameRunner
from pygame.draw import lines as draw_lines, circle as draw_circle, rect as draw_rect, line as draw_line
from core.shape.hex import Hex
# from visual.UI.base.input import InputBase
# from visual.UI.constants.attrs import Attrs
from global_obj import Global


class Body:
    def __init__(self):
        self.hexes = []
        x = 10
        for i in range(10):
            x += 10 * i * 2
            self.hexes.append(Hex(x, 11 * i, 11 * i))
        self.hexes.append(Hex(100, 700, 50))
        self.h = Hex(100, 700, 50)

    def game_loop(self):
        for h in self.hexes:
            draw_lines(Global.display, (100, 100, 100), True, h.dots[1:])
            draw_circle(Global.display, (100, 200, 100), h.center, 2)
            draw_circle(Global.display, (200, 200, 100), h.center, h.r, 1)
            draw_circle(Global.display, (100, 200, 255), h.position, 2)
            draw_circle(Global.display, (255, 100, 100), h.center, h.inner_circle_r, 1)
            draw_rect(Global.display, (255, 255, 255), h.rect, 1)

        self.main_hex()

    def main_hex(self):
        self.h.move_to(Global.mouse.pos)

        c = False
        for h in self.hexes:
            if self.h.collide(h):
                c = True
                draw_line(Global.display, (255, 255, 255), self.h.center, h.center, 3)
                break

        draw_circle(Global.display, (100, 200, 100), self.h.center, 2)
        draw_circle(Global.display, (200, 200, 100), self.h.center, self.h.r, 1)
        draw_circle(Global.display, (100, 200, 255), self.h.position, 2)
        draw_circle(Global.display, (255, 100, 100), self.h.center, self.h.inner_circle_r, 1)
        draw_rect(Global.display, (255, 255, 255), self.h.rect, 1)
        draw_lines(Global.display, (0, 255, 0) if c else (100, 100, 100), True, self.h.dots[1:], 3)


if __name__ == '__main__':
    GameRunner(Body()).run()
