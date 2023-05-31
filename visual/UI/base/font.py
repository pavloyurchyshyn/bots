from pygame import font
from settings.visual.graphic import GraphicConfig

DEFAULT_FONT = font.SysFont(GraphicConfig.DEFAULT_SYS_FONT_NAME, GraphicConfig.FontSize)


def fonts_collector(func):
    memory = {}
    def wrapper(size, font_name=None):
        if (size, font_name) not in memory:
            font_ = func(size, font_name)
            if font_ == DEFAULT_FONT:
                return DEFAULT_FONT
            else:
                memory[(size, font_name)] = font_

        return memory[(size, font_name)]


    return wrapper

@fonts_collector
def get_custom_font(size: int, font_name=None):
    font_name = font_name if font_name else GraphicConfig.DEFAULT_FONT_NAME
    try:
        return font.Font(font_name, int(size))
    except Exception:
        return DEFAULT_FONT

