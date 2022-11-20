from global_obj.logger import get_logger
from core.game_global.stages import Stages
from core.game_global.steps_clock import StepsClock
from core.game_global.id_generator import IdGenerator
from core.game_global.in_game_settings import InGameSettings


class GameGlobal:
    id_generator = IdGenerator()
    stages = Stages(get_logger())

    steps_clock = StepsClock()
    settings = InGameSettings

    skill_pool = None
    details_pool = None
