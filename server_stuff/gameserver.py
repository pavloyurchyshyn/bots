import time
import traceback
from typing import Dict
from _thread import start_new_thread
from global_obj import Global
from core.player import Player
from core.game_logic.game_components.game_data.game_data import GameData
from server_stuff.stages.abs import LogicStageAbs
from server_stuff.stages.game_setup.logic import GameSetup
from game_client.server_interactions.network.connection_wrapper import ConnectionWrapperAbs

LOGGER = Global.logger

TIME = time.time() + 20


class GameServer:
    def __init__(self, server):
        self.server = server
        self.game_data = GameData()
        self.alive = 1
        self.connections: Dict[str, ConnectionWrapperAbs] = {}
        self.players_objs: Dict[str, 'Player'] = {}
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

    def connect(self, response: dict, connection: ConnectionWrapperAbs) -> None:
        """
        Should send all needed things to continue game.
        """
        self.connections[connection.token] = connection
        self.current_stage.connect(response, connection)
        LOGGER.info(f'Final connection response: {response}')
        connection.send_json(response)
        self.start_player_thread(connection=connection)

    def start_player_thread(self, connection: ConnectionWrapperAbs) -> None:
        start_new_thread(self.__player_thread, (connection,))

    def __player_thread(self, connection: ConnectionWrapperAbs) -> None:
        try:
            LOGGER.info(f'Started thread for: {connection.token}')
            self.connected_before.add(connection.token)
            connection.send_json({'ready': True})
            while self.alive and connection.alive:
                player_request = connection.recv_json()
                if player_request:
                    self.current_stage.process_request(player_request, connection)
                    LOGGER.info(f'Request {player_request} from {connection.token}')
                    pass

        except Exception as e:
            LOGGER.critical(f'Failed to thread {connection.token}.')
            LOGGER.error(e)
            LOGGER.error(traceback.format_exc())
