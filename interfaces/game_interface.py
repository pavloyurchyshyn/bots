from typing import Dict, List

from core.player.player import PlayerObj
from core.world.base.logic.world import LogicWorld

from game_logic.bots.bot_player import BotPlayer
from game_logic.game_data.game_settings import GameSettings


class GameInterface(GameSettings):
    bots: List[BotPlayer]
    players: Dict[int, PlayerObj]
    world: LogicWorld
