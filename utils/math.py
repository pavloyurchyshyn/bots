from math import atan2


def get_angle_between_dots(dot_pos_1, dot_pos_2):
    x1, y1 = dot_pos_1
    x2, y2 = dot_pos_2

    d_x = 0.00001 if x2 - x1 == 0.0 else x2 - x1
    d_y = 0.00001 if y2 - y1 == 0.0 else y2 - y1

    return atan2(d_y, d_x)


def dot_in_rect(xy, rx, ry, rh_size, rv_size) -> bool:
    return rx <= xy[0] <= rx + rh_size and ry <= xy[1] <= ry + rv_size
