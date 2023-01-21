import os

os.environ['VisualPygameOn'] = 'off'

import time
import socket
from _thread import start_new_thread
from global_obj.logger import get_logger

from server_stuff.gameserver import GameServer
from server_stuff.server_config import ServerConfig
from server_stuff.constants.start_and_connect import LoginArgs
from game_client.server_interactions.network.socket_connection import SocketConnection
LOGGER = get_logger()


class Server(ServerConfig):
    """
    This part responsible about login, reconnect, etc.
    """

    def __init__(self):
        super(Server, self).__init__()
        self.accepting_connection = True
        self.socket_opened = True
        self.socket = None
        self.address = ''  # socket.gethostbyname(socket.gethostname())
        self.game_server = GameServer(self)

    def run(self):
        self.setup_socket()
        self.handle_connections()
        self.game_server.run()
        LOGGER.info('Game server loop stopped.')

    def setup_socket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.address, self.port))
            self.socket.listen()

        except Exception as e:
            LOGGER.error(e)
            raise e
        else:
            LOGGER.info('Connection successfully opened.')

    def handle_connections(self):
        start_new_thread(self.__handle_connections, ())

    def __handle_connections(self):
        try:
            while self.game_server.alive:
                if not self.accepting_connection:
                    time.sleep(5)
                    continue

                LOGGER.info('Waiting for connection')
                player_connection, (addr, port) = self.socket.accept()
                client_data = SocketConnection.recv_from_connection(player_connection)
                client_data = SocketConnection.recv_to_json(client_data)
                LOGGER.info(f'Client data: {client_data}')
                client_token = client_data.get(LoginArgs.Token)
                is_admin = client_token == self.admin_token

                if client_token in self.game_server.connected_before:
                    LOGGER.info('Player connected before')
                    connection = SocketConnection(LOGGER).set_socket(player_connection)
                    if client_token in self.game_server.connections:
                        client_token = str(hash(str((addr, port))))
                        is_admin = False
                    self.game_server.reassign_player_obj(client_token, client_token)
                    response = {LoginArgs.Connected: True,
                                LoginArgs.Msg: LoginArgs.SuccLogin,
                                LoginArgs.Token: client_token,
                                LoginArgs.IsAdmin: is_admin,
                                }
                    LOGGER.info(f'Simple response: {response}')

                    self.game_server.connect(client_data, response, connection, is_admin)

                elif self.password is None or client_data.get(LoginArgs.Password) == self.password:
                    if is_admin:
                        token = client_token
                    else:
                        token = str(hash(str((addr, port))))

                    connection = SocketConnection(LOGGER)
                    connection.set_socket(player_connection)

                    response = {LoginArgs.Connected: True,
                                LoginArgs.Msg: LoginArgs.SuccLogin,
                                LoginArgs.Token: token,
                                LoginArgs.IsAdmin: is_admin,
                                }
                    LOGGER.info(f'Simple response: {response}')

                    self.game_server.connect(client_data, response, connection, is_admin)

                else:
                    response = {LoginArgs.Connected: False, LoginArgs.Msg: LoginArgs.BadPassword}
                    SocketConnection(LOGGER).set_socket(player_connection).send_json(response)

        except Exception as e:
            LOGGER.error(str(e))
            import traceback
            LOGGER.error(traceback.format_exc())


if __name__ == '__main__':
    try:
        s = Server()
        s.run()
    except Exception as e:
        import traceback
        LOGGER.critical(str(e))
        LOGGER.critical(traceback.format_exc())