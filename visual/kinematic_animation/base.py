from global_obj.main import Global
from typing import Tuple

from pygame.draw import line as draw_line
from pygame.draw import circle as draw_circle
from math import degrees, cos, sin, dist, radians, pi, acos, tan, atan2, sqrt
from utils.math import get_angle_between_dots, get_ray_endpoint


class Joint:
    def __init__(self, name, length, start_pos, color, parent_joint=None, child_joint=None, width: int = 10):
        self.name = name
        self.length = length
        self.width = width
        self.start_pos = start_pos
        self.endpoint = (1, 1)
        self.angle = 0
        self.calculate_endpoint()
        self.color = color
        self.parent_joint: Joint = parent_joint
        self.child_joint: Joint = child_joint

    def change_angle(self, a):
        self.angle = a
        self.calculate_endpoint()
        if self.child_joint:
            self.child_joint.set_start_pos(self.endpoint)

    @property
    def chain_length(self):
        return 1 if self.child_joint is None else self.child_joint.chain_length + 1

    @property
    def structure_length(self):
        return self.length + self.child_joint.structure_length if self.child_joint else self.length

    def calculate_endpoint(self):
        self.endpoint = get_ray_endpoint(start=self.start_pos, angle=self.angle, length=self.length)

    def set_start_pos(self, pos):
        self.start_pos = pos
        self.calculate_endpoint()

    def set_chield(self, chield):
        self.child_joint = chield

    def set_parent(self, parent):
        self.parent_joint = parent

    def draw(self):
        # draw_circle(Global.display, (0, 0, 200), self.start_pos, 7)
        draw_circle(Global.display, (155, 155, 155), self.endpoint, 7)
        draw_line(Global.display, self.color, self.start_pos, self.endpoint, self.width)
        if self.child_joint:
            self.child_joint.draw()


class Arm:
    def __init__(self, pos, arm_len, forearm_len, left=True):
        self.left = left
        self.position = pos
        self.parent_joint = Joint(length=arm_len,
                                  start_pos=self.position,
                                  color=(255, 255, 255),
                                  name='parent',
                                  width=6)
        self.child_joint = Joint(length=forearm_len,
                                 start_pos=self.parent_joint.endpoint,
                                 parent_joint=self.parent_joint,
                                 color=(100, 100, 100),
                                 name='child',
                                 width=3)
        self.parent_joint.set_chield(self.child_joint)

        self.joints_num = self.parent_joint.chain_length
        self.len = self.parent_joint.structure_length

    def update(self, pos):
        dist_to_point = dist(self.position, pos)
        angle = get_angle_between_dots(self.position, pos)

        if dist_to_point >= self.len:
            self.parent_joint.change_angle(angle)
            self.child_joint.change_angle(angle)
        else:
            # https://www.youtube.com/watch?v=nW5FUVzYCKM&ab_channel=KevinMcAleer
            a1 = self.parent_joint.length
            a2 = self.child_joint.length
            x, y = pos
            x1, y1 = self.parent_joint.start_pos
            x -= x1
            y -= y1

            acos_v = (x * x + y * y - a1 * a1 - a2 * a2) / (2 * a1 * a2)
            if acos_v > 1:
                acos_v = 1
            elif acos_v < -1:
                acos_v = -1

            q2 = acos(acos_v)
            if not self.left:
                q2 = -q2

            q1 = atan2(y, x) - atan2(a2 * sin(q2), a1 + a2 * cos(q2))
            self.parent_joint.change_angle(q1)
            self.child_joint.change_angle(q2 + q1)

    @property
    def pos(self) -> Tuple[int, int]:
        return self.position

    @property
    def endpoint(self) -> Tuple[int, int]:
        return self.child_joint.endpoint

    def set_position(self, position):
        self.position = self.parent_joint.start_pos = position

    def add_angle(self, angle: radians):
        self.parent_joint.change_angle(self.parent_joint.angle + angle)
        self.child_joint.change_angle(self.child_joint.angle + angle)

    def draw(self):
        draw_circle(Global.display, (0, 255, 0), self.parent_joint.start_pos, 5)
        self.parent_joint.draw()
