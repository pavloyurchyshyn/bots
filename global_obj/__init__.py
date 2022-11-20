import os
from global_obj.clock import Clock
from global_obj.logger import get_logger

__all__ = 'Global',

VisualPygameOn = os.environ.get('VisualPygameOn', 'off') == 'on'


class Global:
    """
    Object for global ingame parameters.
    """
    logger = get_logger()
    clock = Clock()
    round_clock = Clock()
    test_draw = False

    if VisualPygameOn:
        from global_obj.mouse import Mouse
        from global_obj.keyboard import Keyboard
        from global_obj.display import MAIN_DISPLAY
        from settings.localization import LocalizationLoader
        display = MAIN_DISPLAY
        keyboard = Keyboard(logger)
        mouse = Mouse()
        localization = LocalizationLoader()
