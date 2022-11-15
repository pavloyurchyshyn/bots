from pygame import display, Surface, SRCALPHA, DOUBLEBUF, HWACCEL, FULLSCREEN, SCALED, OPENGL, HWSURFACE, RESIZABLE
from settings.screen.size import SCREEN_H, SCREEN_W

flags = 0  # FULLSCREEN | DOUBLEBUF # | HWSURFACE
MAIN_SCREEN_DEF_COLOR = (0, 0, 0)

MAIN_DISPLAY = display.set_mode((SCREEN_W, SCREEN_H), flags)

MAIN_T_DISPLAY = Surface((SCREEN_W, SCREEN_H), flags, 32)
MAIN_T_DISPLAY.fill((0, 0, 0, 125))
MAIN_T_DISPLAY.convert_alpha()
