from typing import Dict
from core.world.base.logic.world import LogicWorld
from core.player.player import PlayerObj
from game_logic.game_data.game_data import GameData

from game_logic.game_data.game_settings import GameSettings


class Game(GameData):
    def __init__(self, world, setting: GameSettings = GameSettings()):
        self.settings = setting
        super().__init__()
        self.players: Dict[int, PlayerObj] = {}  # player number -> player
        self.map: LogicWorld = world
