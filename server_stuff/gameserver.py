import time
import traceback
from typing import Dict
from _thread import start_new_thread
from global_obj.main import Global

from core.player.player import Player
from core.mech.base.mech import BaseMech
from core.world.base.map_save import MapSave
from core.world.maps_manager import MapsManager
from core.game_logic.game_data.game_data import GameData

from game_client.server_interactions.network.socket_connection import SocketConnection
from game_client.server_interactions.network.socket_connection import ConnectionWrapperAbs

from server_stuff.stages.abs import LogicStageAbs
from server_stuff.stages.game_setup.logic import GameSetup
from server_stuff.stages.game_match.logic import GameMatch
from server_stuff.constants.start_and_connect import LoginArgs
from server_stuff.constants.common import CommonConst
from server_stuff.constants.setup_stage import SetupStgConst as SSC

LOGGER = Global.logger

TIME = time.time() + 130


class GameServer:
    def __init__(self, server):
        self.server = server
        self.maps_mngr = MapsManager()
        self.maps_mngr.load_maps()
        self.current_map: MapSave = self.maps_mngr.maps[0]

        self.game_data = GameData()
        self.alive = 1
        self.players = Global.players_data

        self.connected_before = set()
        self.started_match: bool = False
        self.current_stage: LogicStageAbs = GameSetup(self, self.server)

    def start_game_match(self):
        try:
            Global.logger.info('Start game match')
            game = GameMatch(self, self.server, self.current_map)
            self.started_match = True

            self.send_to_all({SSC.Server.StartMatch: game.get_connection_dict()})
            # todo wait for everybody
            self.current_stage = game
        except Exception as e:
            Global.logger.error('Failed to start game.')
            Global.logger.error(str(e))
            Global.logger.error(traceback.format_exc())
            self.disconnect_all()

    def run(self):
        LOGGER.info('Sever Lobby loop started.')
        while self.alive:
            self.current_stage.update()
            time.sleep(0.1)
            if time.time() > TIME:
                LOGGER.info('Server stopped by timeout.')
                self.alive = False

        LOGGER.info('Server stopped')

    def connect(self, client_data: dict,
                response: dict,
                connection: ConnectionWrapperAbs,
                is_admin: bool,
                player_obj=None) -> None:
        """
        Should send all needed things to continue game.
        """
        # TODO handle error
        token = response[LoginArgs.Token]
        self.connections[token] = connection
        if player_obj is None:
            self.players_objs[token] = player_obj = self.get_player_obj(client_data, token, is_admin)
        response[LoginArgs.Player] = player_obj.get_dict()
        self.current_stage.connect(response, connection)
        LOGGER.debug(f'Final connection response: {response}')
        connection.send_json(response)
        self.start_player_thread(connection=connection, player_obj=self.players_objs[token])

    def get_player_obj(self, client_data: dict, token: str, is_admin: bool) -> Player:
        player = Player(token,
                        nickname=client_data.get(LoginArgs.NickName, 'NoName'),
                        spawn=(10, 10),  # TODO position
                        is_admin=is_admin,
                        mech=BaseMech((10, 10)),
                        actions_count=self.game_data.actions_count,
                        )
        return player

    def start_player_thread(self, connection: ConnectionWrapperAbs, player_obj: Player) -> None:
        start_new_thread(self.__player_thread, (connection, player_obj))

    def __player_thread(self, connection: ConnectionWrapperAbs, player_obj: Player) -> None:
        try:

            LOGGER.info(f'Started thread for: {player_obj.token}')
            self.connected_before.add(player_obj.token)
            while True:
                # wait for ready
                player_request = connection.recv_json()
                if player_request['ready']:
                    self.send_to_all({CommonConst.Chat:
                                          f"{player_obj.nickname} {player_obj.token} connected. Admin {player_obj.is_admin}"})
                    break
                else:
                    # TODO failed to connect
                    return

            # connection.send_json({'ready': True})
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
            self.remove_connection(player_obj.token)
            if self.alive:
                self.send_to_all({CommonConst.Chat: f'{player_obj.nickname} disconnected.'})  # TODO add loc

    def reassign_player_obj(self, from_token: str, to_token: str):
        self.players_objs[to_token] = self.players_objs.pop(from_token)
        Global.logger.info(f'Reassigned player obj from {from_token} to {to_token}')

    def disconnect_all(self):
        for token in tuple(self.connections.keys()):
            self.disconnect(token)
        self.alive = False

    def disconnect(self, token: str):
        connection: SocketConnection = self.connections.pop(token)
        if connection:
            if connection.socket_is_alive:
                connection.send_json({SSC.Server.Disconnect: True})
            connection.close()
            self.connected_before.add(token)

    def send_to_all(self, json_: dict):
        Global.logger.info(f'Send ot all: {json_}')
        for token, connection in self.connections.items():
            if connection.alive:
                try:
                    connection.send_json(json_)
                except Exception as e:
                    Global.logger.warning(f'Failed to send to all to {token}')
        Global.logger.debug(f'Sent ot all: {json_}')

    def remove_connection(self, token: str):
        Global.players_data.connections.pop(token, None)

    @property
    def connections(self) -> Dict[str, SocketConnection]:
        return Global.players_data.connections

    @property
    def players_objs(self) -> Dict[str, Player]:
        return Global.players_data.players_objs

    def get_dict_players_data(self) -> dict:
        return {token: player.get_dict() for token, player in self.players.players_objs.items()}
