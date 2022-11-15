from pygame import Color

EMPTY = Color(0, 0, 0, 0)
HALF_EMPTY = Color(0, 0, 0, 150)
HALF_EMPTY_D = Color(0, 0, 0, 200)
HALF_EMPTY_L = Color(0, 0, 0, 50)

BLUE = [0, 0, 255]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
DARK_GREEN = [0, 55, 0]
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
GREY = [169, 169, 169]
GREY_WHITE = [190, 190, 190]
GREY_DARK = [130, 130, 130]
GREY_DARK_2 = [70, 70, 70]
GREY_DARK_3 = [20, 20, 20]
GREY_DARK_4 = [10, 10, 10]
GREY_GREEN = [160, 255, 160]
GREY_BLUE = [130, 130, 225]
GREY_RED = [255, 130, 130]
UMBRA = [115, 74, 18]
ORANGE = [255, 150, 100]
WHITE_BLUE = [0, 255, 255]
YELLOW = [255, 255, 0]

GOLD = [255, 223, 0]
SILVER = [192, 192, 192]

BULLET_COLOR = [155, 125, 0]


class RedButtonColors:
    text_color = (255, 100, 100)
    button_bord_color = (255, 120, 120)
    button_bord_color_blocked = (90, 90, 90)
    button_back_color = (55, 0, 0)
    button_back_color_blocked = (55, 55, 55)


class CommonColors:
    blue = BLUE
    grey_blue = GREY_BLUE
    red = RED
    green = GREEN
    white = WHITE
    black = BLACK
    grey = GREY_DARK
    grey2 = GREY_DARK_2
    grey3 = GREY_DARK_3
    grey4 = GREY_DARK_4
    yellow = YELLOW
    silver = SILVER


class BarsColors:
    current_energy = (50, 50, 155)
    possible_energy = (150, 150, 255)


simple_colors = CommonColors

BLOOD_COLOR = (75, 0, 0)

PLAYERS_COLORS = {
}
