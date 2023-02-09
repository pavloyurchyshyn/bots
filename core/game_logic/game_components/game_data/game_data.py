from core.game_logic.game_components.game_data.steps_clock import StepsClock
from core.game_logic.game_components.game_data.id_generator import IdGenerator
from core.game_logic.game_components.game_data.game_settings import GameSettings
from core.mech.base.pools import DetailsPool, SkillsPool


class GameData:
    def __init__(self):
        self.players_num: int = 2
        self.steps_clock = StepsClock()
        self.settings = GameSettings()
        self.id_generator: IdGenerator = None
        self.skills_pool: SkillsPool = None
        self.details_pool: DetailsPool = None

