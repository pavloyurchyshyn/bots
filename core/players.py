from typing import Dict, Union
from core.player.abs import PlayerAbs
from game_client.server_interactions.network.socket_connection import SocketConnection


class PlayersData:
    def __init__(self):
        self.connections: Dict[str, SocketConnection] = {}
        self.players_objs: Dict[str, Union['Player', PlayerAbs]] = {}

    def clear(self):
        self.connections.clear()
        self.players_objs.clear()
