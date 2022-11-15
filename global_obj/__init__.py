from global_obj.mouse import Mouse
from global_obj.clock import Clock
from global_obj.logger import LOGGER
from global_obj.id_generator import IdGenerator
from global_obj.display import MAIN_DISPLAY
from global_obj.stages import Stages
from global_obj.keyboard import Keyboard
__all__ = 'Global',


class Global:
    """
    Object for global ingame parameters.
    """
    logger = LOGGER

    clock = Clock()
    round_clock = Clock()
    display = MAIN_DISPLAY
    mouse = Mouse()
    id_generator = IdGenerator()
    stages = Stages(logger)
    keyboard = Keyboard(logger)

