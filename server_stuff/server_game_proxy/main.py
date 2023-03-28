import time
from typing import Dict
from server_stuff.player_client import Client
from server_stuff.server_game_proxy.setup_stage.main import GameSetup
from server_stuff.abs.server import ServerAbc
from core.player.player import PlayerObj
from server_stuff.constants.requests import CommonReqConst

SERVER_LIVE_TIME = 60


class ServerGameProxy:
    def __init__(self, server):
        self.server: ServerAbc = server
        # self.players: Dict[int, PlayerObj] = {}  # todo create players objects
        self.current_stage = GameSetup(self, self.server)

    def run(self):
        a = time.time() + SERVER_LIVE_TIME
        while time.time() < a:
            time.sleep(0.1)
        print('end of game')

    def connect(self, response: dict, client: Client):
        self.current_stage.connect(response=response, client=client)
        response.update(self.get_connected_players_dict())

    def process_player_request(self, client: Client, request: dict):
        self.current_stage.process_request(request, client)

    def get_connected_players_dict(self) -> dict:
        clients = {client.token: (self.current_stage.game_logic.players_slots.get(client.token), client.nickname)
                   for client in
                   self.server.alive_connections.values()}
        return {CommonReqConst.ConnectedPlayers: clients}

    def get_players_slots_dict(self) -> dict:
        slots = {}
        for slot, v in self.current_stage.game_logic.players_slots.items():
            if v in self.server.alive_connections:
                nickname = self.server.alive_connections[v].nickname
            else:
                nickname = ''

            slots[slot] = (v, nickname)

        return {CommonReqConst.PlayersSlots: slots}
