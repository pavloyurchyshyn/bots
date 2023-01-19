from core.player import Player
from game_client.server_interactions.network.socket_connection import ConnectionWrapperAbs
from server_stuff.stages.abs import LogicStageAbs
# TODO
class GameMatch(LogicStageAbs):
    def update(self):
        pass

    def process_request(self, request: dict, connection: ConnectionWrapperAbs, player_obj: Player):
        pass

    def connect(self, response: dict, connection: ConnectionWrapperAbs):
        pass
