from typing import Dict, List

from core.player.player import PlayerObj
from core.world.base.logic.world import LogicWorld

from game_logic.bots.bot_player import BotPlayer
from game_logic.game_data.game_data import GameData
from game_logic.game_data.game_settings import GameSettings


class Game(GameData):
    def __init__(self,
                 world: LogicWorld,
                 setting: GameSettings,
                 players: Dict[int, PlayerObj],
                 bots: List[BotPlayer],
                 ):
        self.settings: GameSettings = setting
        super().__init__()
        self.bots = bots
        self.players: Dict[int, PlayerObj] = players  # player number -> player
        self.world: LogicWorld = world
