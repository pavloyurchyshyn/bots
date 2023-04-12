from typing import Dict, List

from core.player.player import PlayerObj
from core.world.base.logic.world import LogicWorld

from game_logic.bots.bot_player import BotPlayer
from game_logic.game_data.game_data import GameData
from game_logic.game_data.game_settings import GameSettings


class GameInterface(GameData):
    bots: List[BotPlayer]
    players: Dict[int, PlayerObj]
    world: LogicWorld
    settings: GameSettings
