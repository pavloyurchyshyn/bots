import os
from global_obj.clock import Clock
from global_obj.logger import get_logger
from global_obj.stages import Stages

__all__ = 'Global',

VisualPygameOn = os.environ.get('VisualPygameOn', 'off') == 'on'


class Global:
    """
    Object for global ingame parameters.
    """
    logger = get_logger()
    clock = Clock()
    stages = Stages(logger)
    round_clock = Clock()
    test_draw = True

    if VisualPygameOn:
        from global_obj.mouse import Mouse as __mouse
        from global_obj.keyboard import Keyboard as __keyboard
        from global_obj.display import MAIN_DISPLAY as __display
        from settings.localization import LocalizationLoader as __localization
        display = __display
        keyboard = __keyboard(logger)
        mouse = __mouse()
        localization = __localization()
