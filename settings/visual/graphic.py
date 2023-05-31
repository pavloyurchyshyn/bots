from settings.screen.size import scaled_w
from settings.base import ROOT_OF_GAME
from settings.json_configs_manager import save_to_common_config, get_and_save_from_common_config


class GraphicConfig:
    DEFAULT_SYS_FONT_NAME = 'Arial'
    DEFAULT_FONT_SIZE = scaled_w(0.0078125)
    DEFAULT_FONT_NAME = str(ROOT_OF_GAME / 'fonts' / 'Xolonium-Regular.otf')

    Antialiasing = get_and_save_from_common_config('Antialiasing', False)
    AntialiasingText = get_and_save_from_common_config('AntialiasingText', True)
    FontSize = get_and_save_from_common_config('FontSize', DEFAULT_FONT_SIZE)
    FontName = get_and_save_from_common_config('FontName', DEFAULT_FONT_NAME)

    @classmethod
    def set_antialiasing(cls, value: bool):
        save_to_common_config('Antialiasing', value)
        cls.Antialiasing = value

    @classmethod
    def set_antialiasing_text(cls, value: bool):
        save_to_common_config('AntialiasingText', value)
        cls.AntialiasingText = value

    @classmethod
    def set_font_size(cls, value: bool):
        save_to_common_config('FontSize', value)
        cls.FontSize = value

    @classmethod
    def set_font_name(cls, value: bool):
        save_to_common_config('FontName', value)
        cls.FontName = value
