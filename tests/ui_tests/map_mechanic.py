import math
import collections
from launch import GameRunner
from visual.UI.utils import get_surface
from global_obj.main import Global
from pygame.draw import lines as draw_lines, circle as draw_circle, rect as draw_rect, line as draw_line, \
    polygon as draw_pol
from visual.UI.base.font import get_custom_font

FONT = get_custom_font(9)

Axial = collections.namedtuple('Axial', ['q', 'r'])
Cube = collections.namedtuple('Cube', ['q', 'r', 's'])


def cube_to_axial(cube: Cube):
    return Axial(cube.q, cube.r)


def axial_to_cube(ax: Axial):
    return Cube(ax.q, ax.r, -ax.q - ax.r)


class HexCoord:
    def __init__(self, x, y, q, r):
        self.x = x
        self.y = y

        self.q = q
        self.r = r
        # self.s = -self.q - self.r

        if self.r > 0:
            self.z = self.r - (self.q - (self.q << 1)) / 2
        else:
            self.z = self.r - (self.q + (self.q << 1)) / 2

        self.s = int(-self.x - self.z)

    @property
    def qrs(self):
        return self.q, self.r, self.s


cube_direction_vectors = [
    Cube(+1, 0, -1), Cube(+1, -1, 0), Cube(0, -1, +1),
    Cube(-1, 0, +1), Cube(-1, +1, 0), Cube(0, +1, -1),
]

PREPARED_ANGLES = [math.radians(30 + 60 * i) for i in range(6)]


def get_hex_width(r):
    return r + r


def get_hex_distance(r):
    return get_hex_width(r) * 0.75


def get_hex_height(r):
    return math.sqrt(3) * r


def get_hex_center(x, y, r):
    x0 = x * get_hex_distance(r) + get_hex_width(r) / 2
    y0 = y * get_hex_height(r) + get_hex_height(r) / 2
    y0 = (y + (0. if x % 2 else 0.5)) * get_hex_height(r) + get_hex_height(r) / 2
    return x0, y0


def get_hex_lt(x, y, r):
    x, y = get_hex_center(x, y, r)
    x -= get_hex_width(r) / 2
    y -= get_hex_height(r) / 2
    return x, y


def get_indexes_from_coordinates(x, y, r):
    x = x // get_hex_distance(r)
    if x % 2 != 0.:
        y = y + get_hex_height(r) * 0.5
    y = ((y - get_hex_height(r) / 2) // get_hex_height(r))
    return int(x), int(y)


def normalize_pos(x, y, r):
    return get_hex_center(*get_indexes_from_coordinates(x, y, r), r)


def get_dots(x, y, r, dx=0, dy=0):
    x, y = get_hex_center(x, y, r)
    return [(int(x + dx + r * math.cos(a)), int(y + dy + r * math.sin(a))) for a in PREPARED_ANGLES]


class Body:
    def __init__(self):
        self.r = 30
        self.rad = 1
        self.dx, self.dy = 0, 0

        self.x_size = x_size = 30
        self.y_size = y_size = 15
        self.surface = get_surface(*Global.display.get_hex_size())
        # self.surface = get_surface(get_hex_distance(self.r) * (x_size + 0.25) + 5,
        #                            get_hex_height(self.r) * (y_size + 0.5) + 1)

        self.hexes = []
        self.hexes_coords = {}
        self.hexes_cube_coords = {}

        self.mid_x = mid_x = x_size // 2
        self.mid_y = mid_y = y_size // 2
        print(mid_x, mid_y)
        for y in range(y_size + 1):
            for x in range(x_size + 1):
                # h = HexCoord(x, y, q=x - mid_x, r=y - mid_y)
                h = HexCoord(x, y, q=x, r=y)
                self.hexes.append(h)
                self.hexes_coords[(x, y)] = h
                self.hexes_cube_coords[(h.q, h.r, h.s)] = h
        self.render()

    def game_loop(self):
        Global.display.blit(self.surface, (self.dx, self.dy))
        self.draw_normalized_mouse()
        draw_circle(Global.display, (255, 255, 255), Global.mouse.pos, 1)
        pos = get_indexes_from_coordinates(Global.mouse.x_real - self.dx, Global.mouse.y_real - self.dy, self.r)
        if Global.mouse.l_up:
            self.rad += 1
        elif Global.mouse.r_up:
            self.rad -= 1

        if pos in self.hexes_coords:
            self.draw_collided_hex(pos)
            self.square(self.hexes_coords[pos])
            # self.draw_lines(pos)
            # self.draw_neighbors_by_xy(pos)
            # self.draw_neighbors_by_qrs(pos)

    def square(self, h):
        r = self.rad
        print('=' * 10, r)

        # prev_a = 0
        # for a in range(30, 361, 30):
        #     x = int(r * math.cos(math.radians(a)))
        #     y = int(r * math.sin(math.radians(prev_a)))
        #     for x_ in range(*(0, x + 1) if x > 0 else (x, 0)):
        #         for y_ in range(*(0, y + 1) if y > 0 else (y, 0)):
        #
        #             coord = (h.x + x_, h.y + y_)
        #             print(a, (x, y), coord)
        #
        #             if coord in self.hexes_coords:
        #                 self.draw_tile_borders(Global.display,
        #                                        get_dots(*coord, self.r, self.dx, self.dy),
        #                                        color=(255, 100, 100),
        #                                        width=5)
        #
        #     prev_a = a

        # for y in range(-r, r + 1):
        #     dx = r  # - abs(y) + (1 if y != 0 else -1)
        #     print(f"r={r}", f"dy={y}", f"dx={dx}", (-dx, dx), '->', tuple(range(-dx, 1 + dx)))
        #     for x in range(-dx, dx + 1):
        #         if math.dist((h.x, h.y), (h.x + x, h.y + y)) >= math.dist((h.x, h.x), (h.x + r, h.y + r)):
        #             continue
        #         # if h.x % 2 and x % 2 != 0 and y == r:
        #         #     continue
        #         # elif h.x % 2 == 0 and x % 2 != 0 and y == -r:
        #         #     continue
        #         # elif x % 2 and y == -x:
        #         #     continue
        #
        #         coord = h.x + x, h.y + y
        #         if coord in self.hexes_coords:
        #             self.draw_tile_borders(Global.display,
        #                                    get_dots(*coord, self.r, self.dx, self.dy),
        #                                    color=(255, 100, 100),
        #                                    width=5)

    def draw_lines(self, pos):
        h = self.hexes_coords[pos]
        color = (255, 255, 255)
        # hexes = []
        # coords = [h.x, h.y]
        # self.hexes_cube_coords[(h.q, h.r, h.s)]
        for y in range(-1, 2):
            for x in range(-1, 2):
                coords = [h.x, h.y]

                while tuple(coords) in self.hexes_coords and (x != 0 and y != 0):
                    nh = self.hexes_coords[tuple(coords)]
                    # for nh in hexes:
                    self.draw_tile_borders(Global.display,
                                           get_dots(nh.x_real, nh.y_real, self.r, self.dx, self.dy),
                                           color=color,
                                           width=3)
                    coords[0] -= 1 * y * x

                    if y > 0:
                        coords[1] -= 0 if coords[0] % 2 else 1
                    else:
                        coords[1] += 1 if coords[0] % 2 else 0

        # for y in (-1, 1):
        #     coords = [h.x, h.y]
        #
        #     while tuple(coords) in self.hexes_coords:
        #         # for
        #         nh = self.hexes_coords[tuple(coords)]
        #         # for nh in hexes:
        #         self.draw_tile_borders(Global.display,
        #                                get_dots(nh.x, nh.y, self.r, self.dx, self.dy),
        #                                color=color,
        #                                width=2)
        #         coords[0] += y
        #         if y > 0:
        #             coords[1] += (1 if coords[0] % 2 else 0)
        #         else:
        #             coords[1] += (1 if coords[0] % 2 else 0)

    # def draw_neighbors_by_qrs(self, pos):
    #     h = self.hexes_coords[pos]
    #     vectors = cube_direction_vectors
    #     for vec in vectors:
    #         n_pos = (h.q + vec[0], h.r + vec[1], h.s + vec[2])
    #         if n_pos in self.hexes_cube_coords:
    #             nh = self.hexes_cube_coords[n_pos]
    #             self.draw_tile_borders(Global.display,
    #                                    get_dots(nh.x, nh.y, self.r, self.dx, self.dy),
    #                                    color=(155, 155, 255),
    #                                    width=2)

    def draw_neighbors_by_xy(self, pos):
        x, y = pos
        if x % 2:
            n_coords = ((-1, -1), (0, -1),
                        (+1, -1), (+1, 0),
                        (0, +1), (-1, 0),)
        else:
            n_coords = ((+1, 0), (0, -1),
                        (-1, 0), (-1, +1),
                        (0, +1), (+1, +1),)

        for (dx, dy) in n_coords:
            neighbor_pos = x + dx, y + dy
            if neighbor_pos in self.hexes_coords:
                nh = self.hexes_coords[neighbor_pos]
                self.draw_tile_borders(Global.display,
                                       get_dots(nh.x, nh.y + abs(nh.x - self.mid_x), self.r, self.dx, self.dy),
                                       color=(155, 255, 155),
                                       width=3)

    def draw_normalized_mouse(self):
        draw_circle(Global.display, (255, 0, 0), self.normalize_mouse(), 3)

    def draw_collided_hex(self, pos):
        self.draw_tile_borders(Global.display, get_dots(*pos, self.r, self.dx, self.dy), width=3)

    def normalize_mouse(self) -> tuple:
        x, y = normalize_pos(Global.mouse.x_real - self.dx, Global.mouse.y_real - self.dy, self.r)
        return x + self.dx, y + self.dy

    def render(self):
        self.surface.fill((0, 0, 0))
        for h in self.hexes:
            self.draw_tile(self.surface, h)

    def draw_tile(self, surface, h):
        dy = 0  # +(abs(h.x - self.mid_x))  # // 2
        dots = get_dots(h.x_real, h.y_real + dy, self.r)

        draw_pol(surface, (55, 55, 55), dots)
        self.draw_text(surface, h, dy)
        self.draw_tile_borders(surface, dots, 3 if h.qrs == (0, 0, 0) else 1)

    def draw_text(self, surface, h, dy):
        x_y_text = FONT.render(str((h.x_real, h.y_real)), True, (255, 255, 255))
        x, y = get_hex_center(h.x_real, h.y_real + dy, self.r)
        surface.blit(x_y_text, (x - x_y_text.get_width() // 2, y - x_y_text.get_height() // 2))
        qrs_text = FONT.render(str((h.s, h.q, h.r)), True, (255, 255, 255))
        surface.blit(qrs_text, (x - qrs_text.get_width() // 2, y + x_y_text.get_height() // 2))

    def draw_tile_borders(self, surface, dots, color=(155, 155, 155), width=1):
        draw_lines(surface, color, True, dots, width)


if __name__ == '__main__':
    # x, y, r = 10, 10, 10
    # print(x, y)
    # x, y = get_hex_center(x, y, r)
    # print(x, y)
    #
    # x, y = normalize_pos(x, y, r)
    # print(x, y)

    GameRunner(Body()).run()
