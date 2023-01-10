from typing import Dict
from core.world.base.logic.world import LogicWorld
from core.game_logic.game_components.game_data.game_data import GameData


class Game(GameData):
    def __init__(self, world):
        super().__init__()
        self.players: Dict[str, 'Player'] = {}
        self.map: LogicWorld = world
