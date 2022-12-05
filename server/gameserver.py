import time
import traceback
from typing import Dict
from _thread import start_new_thread
from server.connection_wrapper import ConnectionWrapperAbs
from global_obj.logger import get_logger
from core.game_logic.game_data.game_settings import GameSettings

LOGGER = get_logger()

TIME = time.time() + 20


class GameServer:
    def __init__(self, server):
        self.server = server
        self.settings = GameSettings()
        self.alive = 1
        self.connections: Dict[str, ConnectionWrapperAbs] = {}
        self.connected_before = set()

    def run(self):
        LOGGER.info('Sever Lobby loop started.')
        while self.alive:
            time.sleep(5)
            # HERE SHOULD BE GAME LOGIC
            if time.time() > TIME:
                self.alive = False
                LOGGER.info('Server stopped')

    def reconnect(self, connection: ConnectionWrapperAbs) -> None:
        self.connections[connection.token] = connection

    def star_player_thread(self, connection: ConnectionWrapperAbs) -> None:
        start_new_thread(self.__player_thread, (connection,))

    def __player_thread(self, connection: ConnectionWrapperAbs) -> None:
        try:
            LOGGER.info(f'Started thread for: {connection.token}')
            self.connected_before.add(connection.token)
            connection.send_json({'ready': True})
            while self.alive and connection.alive:
                player_request = connection.recv_json()
                if player_request:
                    # process_request(player_request, connection.token)
                    LOGGER.info(f'Request {player_request} from {connection.token}')
                    pass

        except Exception as e:
            LOGGER.critical(f'Failed to thread {connection.token}.')
            LOGGER.error(e)
            LOGGER.error(traceback.format_exc())
