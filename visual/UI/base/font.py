from pygame import font
from settings.screen.size import scaled_w

DEFAULT_FONT_NAME = 'Arial'
DEFAULT_FONT_SIZE = scaled_w(0.0078125)


def get_custom_font(size: int, font_name=None):
    font_name = font_name if font_name else DEFAULT_FONT_NAME
    return font.SysFont(font_name, int(size))


DEFAULT_FONT = font.SysFont(DEFAULT_FONT_NAME, DEFAULT_FONT_SIZE)
