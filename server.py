import os

os.environ['VisualPygameOn'] = 'off'

import time
import socket
from _thread import start_new_thread
from global_obj.logger import get_logger

LOGGER = get_logger()
from server_stuff.server_config import ServerConfig
from server_stuff.constants.start_and_connect import LoginArgs
from server_stuff.gameserver import GameServer
from game_client.server_interactions.network.connection_wrapper import SocketConnectionWrapper


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
                client_data = SocketConnectionWrapper.recv_from_connection(player_connection)
                client_data = SocketConnectionWrapper.recv_to_json(client_data)
                LOGGER.info(f'Client data: {client_data}')
                if client_data.get(LoginArgs.Token) in self.game_server.connected_before:
                    token = client_data[LoginArgs.Token]
                    connection = SocketConnectionWrapper(player_connection, token)
                    response = {LoginArgs.Connected: True,
                                LoginArgs.Msg: LoginArgs.SuccLogin,
                                LoginArgs.Token: token,
                                LoginArgs.IsAdmin: self.admin_token == token,
                                }
                    self.game_server.connect(response, connection)

                elif self.password is None or client_data.get(LoginArgs.Password) == self.password:
                    if client_data[LoginArgs.Token] == self.admin_token:
                        token = client_data[LoginArgs.Token]
                    else:
                        token = str(hash(str((addr, port))))
                    connection = SocketConnectionWrapper(player_connection, token)
                    response = {LoginArgs.Connected: True,
                                LoginArgs.Msg: LoginArgs.SuccLogin,
                                LoginArgs.Token: token,
                                LoginArgs.IsAdmin: self.admin_token == token,
                                }
                    self.game_server.connect(response, connection)

                else:
                    response = {LoginArgs.Connected: False, LoginArgs.Msg: LoginArgs.BadPassword}
                    SocketConnectionWrapper(connection=player_connection).send_json(response)

        except Exception as e:
            LOGGER.error(str(e))
            import traceback
            LOGGER.error(traceback.format_exc())


if __name__ == '__main__':
    try:
        s = Server()
        s.run()
    except Exception as e:
        LOGGER.critical(str(e))
