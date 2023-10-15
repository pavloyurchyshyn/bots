from launch import GameRunner
from global_obj.main import Global
from typing import Tuple

from utils.math import get_angle_between_dots, get_ray_endpoint

from pygame.surface import Surface
from pygame.transform import rotate
from pygame.draw import line as draw_line
from pygame.draw import circle as draw_circle
from math import degrees, cos, sin, dist, radians, pi, acos, tan, atan2, sqrt
from visual.kinematic_animation.base import Joint, Arm
from visual.UI.utils import get_surface


def draw_ray(start: tuple, angle, length, color=(255, 200, 200)):
    draw_line(Global.display, color, start, get_ray_endpoint(start, angle=angle, length=length), 2)


class Body:
    def __init__(self, position: tuple[int, int], size: int):
        self.size = size
        self.position = position
        self.angle = 0
        arm_len, forearm_len = 40, 30

        self.left_arm: Arm = Arm(pos=position, left=True, arm_len=arm_len, forearm_len=forearm_len)
        self.right_arm: Arm = Arm(pos=position, left=False, arm_len=arm_len, forearm_len=forearm_len)
        self.sword: Sword = Sword(self.right_arm.endpoint)
        self.define_arms_positions()

    def update(self):
        if Global.mouse.m_pressed:
            self.change_angle(get_angle_between_dots(self.position, Global.mouse.pos))

        if Global.mouse.l_pressed:
            self.left_arm.update(Global.mouse.pos)
        if Global.mouse.r_pressed:
            self.right_arm.update(Global.mouse.pos)

    def change_angle(self, angle: radians):
        d_angle = angle - self.angle
        self.angle = angle
        self.right_arm.add_angle(d_angle)
        self.left_arm.add_angle(d_angle)
        self.define_arms_positions()

    def define_arms_positions(self):
        self.left_arm.set_position(get_ray_endpoint(self.position, self.angle - radians(90), self.size))
        self.right_arm.set_position(get_ray_endpoint(self.position, self.angle + radians(90), self.size))

        self.sword.set_angle(-degrees(self.right_arm.child_joint.angle) + 90)
        self.sword.set_position(self.right_arm.endpoint)

    def draw(self):
        draw_circle(Global.display, (100, 100, 100), self.position, self.size)
        draw_ray(self.position, self.angle, self.size)
        self.left_arm.draw()
        self.right_arm.draw()

        self.sword.draw()


class Sword:
    def __init__(self, xy):
        self.pos = xy
        self.lt = xy
        self.a = 0
        self.image: Surface = get_surface(100, 100, color=(100, 100, 100))
        self.original_image: Surface = self.image
        draw_line(self.image, (255, 255, 255), (50, 0), (50, 100), 5)

        self.define_position()

        # self.sword.fill((255, 255, 255))
        self.image.get_rect().center = (5, 0)

    def define_position(self):
        x, y = self.pos
        angle = self.a
        self.image = rotate(self.original_image, self.a)
        #l_1 = self.image.get_width()
        #l_2 = self.image.get_height()
        #x, y = int(start[0] + cos(angle) * l_1) - self.image.get_width() // 2, int(start[1] + sin(angle) * l_2)
        self.lt = x, y

    def set_angle(self, angle):
        self.a = angle
        self.image = rotate(self.original_image, self.a)

    def set_position(self, pos: tuple):
        self.pos = pos
        self.define_position()

    def draw(self, surface: Surface = None):
        surface = surface if surface else Global.display
        surface.blit(self.image, self.lt)
        draw_circle(surface, (0, 255, 0), self.lt, 5, 0)


class Animation:
    def __init__(self, mech: Body, duration: int = 3):
        self.mech: Body = mech
        self.duration = duration


class GameBody:
    def __init__(self):
        self.mech = Body((500, 500), size=25)
        self.a = 0

    def game_loop(self):
        Global.display.fill((10, 10, 10))
        self.mech.update()
        self.mech.draw()


def close():
    from pygame import quit as close_program_pygame
    import sys

    close_program_pygame()
    sys.exit()


if __name__ == '__main__':
    game_body = GameBody()
    game_runner = GameRunner(game_body=game_body)
    game_runner.run()
