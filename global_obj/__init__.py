import os
from global_obj.clock import Clock
from global_obj.logger import LOGGER

__all__ = 'Global',

VisualPygameOn = os.environ.get('VisualPygameOn', 'off') == 'on'


class Global:
    """
    Object for global ingame parameters.
    """
    logger = LOGGER
    clock = Clock()
    round_clock = Clock()

    if VisualPygameOn:
        from global_obj.mouse import Mouse
        from global_obj.keyboard import Keyboard
        from global_obj.display import MAIN_DISPLAY
        display = MAIN_DISPLAY
        keyboard = Keyboard(logger)
        mouse = Mouse()
