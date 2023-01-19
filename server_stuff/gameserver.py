import time
import traceback
from typing import Dict
from _thread import start_new_thread

from global_obj.main import Global

from core.player import Player
from core.world.base.map_save import MapSave
from core.world.maps_manager import MapsManager
from core.game_logic.game_components.game_data.game_data import GameData

from game_client.server_interactions.network.socket_connection import SocketConnection
from game_client.server_interactions.network.socket_connection import ConnectionWrapperAbs

from server_stuff.stages.abs import LogicStageAbs
from server_stuff.stages.game_setup.logic import GameSetup
from server_stuff.stages.game_match.logic import GameMatch
from server_stuff.constants.start_and_connect import LoginArgs
from server_stuff.constants.setup_stage import SetupStgConst as SSC

LOGGER = Global.logger

TIME = time.time() + 60


class GameServer:
    def __init__(self, server):
        self.server = server
        self.maps_mngr = MapsManager()
        self.maps_mngr.load_maps()
        self.current_map: MapSave = self.maps_mngr.maps[0]

        self.game_data = GameData()
        self.alive = 1
        self.connections: Dict[str, SocketConnection] = {}
        self.players_objs: Dict[str, Player] = {}
        self.connected_before = set()
        self.started_match: bool = False
        self.current_stage: LogicStageAbs = GameSetup(self, self.server)

    def start_game_match(self):
        Global.logger.info('Start game match')
        self.started_match = True
        self.send_to_all({
            SSC.Server.StartMatch: {
                SSC.Server.MatchArgs.Map: self.current_map.get_save_dict()
            },
        }
        )

    def run(self):
        LOGGER.info('Sever Lobby loop started.')
        while self.alive:
            time.sleep(0.1)
            self.current_stage.update()

            if time.time() > TIME:
                LOGGER.info('Server stopped by timeout.')
                self.alive = False

        LOGGER.info('Server stopped')

    def connect(self, client_data: dict, response: dict, connection: ConnectionWrapperAbs, is_admin: bool) -> None:
        """
        Should send all needed things to continue game.
        """
        token = response[LoginArgs.Token]
        self.connections[token] = connection
        self.players_objs[token] = self.get_player_obj(client_data, token, is_admin)
        self.current_stage.connect(response, connection)
        LOGGER.debug(f'Final connection response: {response}')
        connection.send_json(response)
        self.start_player_thread(connection=connection, player_obj=self.players_objs[token])

    def get_player_obj(self, client_data: dict, token: str, is_admin: bool) -> Player:
        player = Player(token,
                        client_data.get(LoginArgs.NickName, 'NoName'),
                        is_admin,
                        )
        return player

    def start_player_thread(self, connection: ConnectionWrapperAbs, player_obj: Player) -> None:
        start_new_thread(self.__player_thread, (connection, player_obj))

    def __player_thread(self, connection: ConnectionWrapperAbs, player_obj: Player) -> None:
        try:

            LOGGER.info(f'Started thread for: {player_obj.token}')
            self.connected_before.add(player_obj.token)
            connection.send_json({'ready': True})
            while self.alive and connection.alive:
                player_request = connection.recv_json()
                if player_request:
                    LOGGER.info(f'Request {player_request} from {player_obj.token}')
                    self.current_stage.process_request(request=player_request,
                                                       connection=connection,
                                                       player_obj=player_obj)
                    LOGGER.info(f'Request processed.')

        except Exception as e:
            LOGGER.critical(f'Failed to thread {player_obj.token}.')
            LOGGER.error(e)
            LOGGER.error(traceback.format_exc())

    def reassign_player_obj(self, from_token: str, to_token: str):
        self.players_objs[to_token] = self.players_objs.pop(from_token)
        Global.logger.info(f'Reassigned player obj from {from_token} to {to_token}')

    def disconnect(self, token: str):
        connection: SocketConnection = self.connections.pop(token)
        if connection:
            if connection.socket_is_alive:
                connection.send_json({SSC.Server.Disconnect: True})
            connection.close()
            self.connected_before.add(token)

    def send_to_all(self, json_: dict):
        Global.logger.debug(f'Send ot all: {json_}')
        for connection in self.connections.values():
            if connection.alive:
                connection.send_json(json_)
        Global.logger.info(f'Sent ot all: {json_}')
