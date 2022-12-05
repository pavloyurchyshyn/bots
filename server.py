import time
import socket
from _thread import start_new_thread
from global_obj.logger import get_logger
from server.server_config import ServerConfig
from constants.server.start_and_connect import LoginArgs
from server.gameserver import GameServer
from server.connection_wrapper import SocketConnectionWrapper

LOGGER = get_logger()


class Server(ServerConfig):
    def __init__(self):
        super(Server, self).__init__()
        self.accepting_connection = True
        self.socket_opened = True
        self.socket = None
        self.address = socket.gethostbyname(socket.gethostname())
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
                if client_data.get(LoginArgs.Token) == self.game_server.connected_before:
                    self.game_server.reconnect(SocketConnectionWrapper(player_connection, client_data[LoginArgs.Token]))
                elif self.password is None or client_data.get(LoginArgs.Password) == self.password:
                    token = str(hash(str((addr, port))))
                    connection = SocketConnectionWrapper(player_connection, token)
                    connection.send_json({LoginArgs.Connected: True,
                                          LoginArgs.Msg: LoginArgs.SuccLogin,
                                          LoginArgs.Token: token,
                                          })
                    self.game_server.star_player_thread(connection=connection)
                else:
                    response = {LoginArgs.Connected: False, LoginArgs.Msg: LoginArgs.BadPassword}
                    SocketConnectionWrapper(connection=player_connection).send_json(response)

        except Exception as e:
            LOGGER.error(str(e))
            import traceback
            LOGGER.error(traceback.format_exc())


if __name__ == '__main__':
    s = Server()
    s.run()
