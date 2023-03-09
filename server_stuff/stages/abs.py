from abc import abstractmethod
from core.player.player import Player
from game_logic.game_data.game_data import GameData
from game_logic.game_data.game_settings import GameSettings
from game_client.server_interactions.socket_connection import ConnectionWrapperAbs


class LogicStageAbs:
    def __init__(self, game_server, server):
        self.game_server = game_server
        self.server = server
        self.game_data: GameData = game_server.game_data
        self.settings: GameSettings = game_server.game_data.settings

    @abstractmethod
    def update(self):
        raise NotImplementedError

    @abstractmethod
    def process_request(self, request: dict, connection: ConnectionWrapperAbs, player_obj: Player):
        raise NotImplementedError

    @abstractmethod
    def connect(self, response: dict, connection: ConnectionWrapperAbs):
        raise NotImplementedError
