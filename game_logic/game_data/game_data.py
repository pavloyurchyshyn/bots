from game_logic.game_data.steps_clock import StepsClock
from game_logic.game_data.id_generator import IdGenerator
from core.mech.base.pools import DetailsPool, SkillsPool
from game_logic.game_data.game_settings import GameSettings


class GameData:
    settings: GameSettings

    def __init__(self):
        self.real_players_num: int = self.settings.real_players_num
        self.players_num: int = self.settings.players_num
        self.players_ready: int = 0
        self.steps_clock = StepsClock(self.settings.actions_count)
        self.id_generator: IdGenerator = IdGenerator(self.settings.seed)
        self.details_pool: DetailsPool = DetailsPool(self.id_generator)
        self.skills_pool: SkillsPool = self.details_pool.skills_pool
