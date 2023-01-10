from abc import abstractmethod
from game_client.server_interactions.network.connection_wrapper import ConnectionWrapperAbs
from core.game_logic.game_components.game_data.game_settings import GameSettings


class LogicStageAbs:
    def __init__(self, game_server, server):
        self.game_server = game_server
        self.server = server
        self.game_data = game_server.game_data
        self.settings: GameSettings = game_server.game_data.settings

    @abstractmethod
    def update(self):
        raise NotImplementedError

    @abstractmethod
    def process_request(self, request: dict, connection: ConnectionWrapperAbs):
        raise NotImplementedError

    @abstractmethod
    def connect(self, response: dict, connection: ConnectionWrapperAbs):
        raise NotImplementedError
