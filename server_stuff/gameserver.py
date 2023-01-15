import time
import traceback
from typing import Dict
from _thread import start_new_thread
from global_obj.main import Global
from core.game_logic.game_components.game_data.game_data import GameData
from server_stuff.stages.abs import LogicStageAbs
from server_stuff.stages.game_setup.logic import GameSetup
from game_client.server_interactions.network.socket_connection import ConnectionWrapperAbs
from core.world.maps_manager import MapsManager
from core.player import Player
from server_stuff.constants.start_and_connect import LoginArgs

LOGGER = Global.logger

TIME = time.time() + 20


class GameServer:
    def __init__(self, server):
        self.server = server
        self.maps_mngr = MapsManager()
        self.maps_mngr.load_maps()
        self.current_map = self.maps_mngr.maps[0]

        self.game_data = GameData()
        self.alive = 1
        self.connections: Dict[str, ConnectionWrapperAbs] = {}
        self.players_objs: Dict[str, Player] = {}
        self.connected_before = set()

        self.current_stage: LogicStageAbs = GameSetup(self, self.server)

    def run(self):
        LOGGER.info('Sever Lobby loop started.')
        while self.alive:
            time.sleep(0.1)
            self.current_stage.update()
            # LOGGER.info('event')
            if time.time() > TIME:
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

    def send_to_all(self, json_: dict):
        Global.logger.info(f'Send ot all: {json_}')
        for connection in self.connections.values():
            if connection.alive:
                connection.send_json(json_)
        Global.logger.info(f'Sent ot all: {json_}')
