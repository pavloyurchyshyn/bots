from game_logic.game_data.steps_clock import StepsClock
from game_logic.game_data.id_generator import IdGenerator
from game_logic.game_data.game_settings import GameSettings
from core.mech.base.pools import DetailsPool, SkillsPool


class GameData:
    def __init__(self):
        self.players_num: int = 2
        self.players_ready: int = 0
        self.steps_clock = StepsClock()
        self.settings = GameSettings()
        self.id_generator: IdGenerator = None
        self.skills_pool: SkillsPool = None
        self.details_pool: DetailsPool = None
        self.actions_count: int = 3

