import time
import socket

from abc import abstractmethod
from settings.network import NetworkData
from global_obj.logger import get_logger
from constants.server.start_and_connect import LoginArgs
from server.connection_wrapper import SocketConnectionWrapper, ConnectionWrapperAbs


LOGGER = get_logger()


class NetworkAbs:
    connection: ConnectionWrapperAbs
    connected: bool

    @abstractmethod
    def connect(self):
        raise NotImplementedError

    @abstractmethod
    def disconnect(self):
        raise NotImplementedError


class SocketConnectionNetwork(NetworkData, NetworkAbs):
    def __init__(self):
        super(SocketConnectionNetwork, self).__init__()
        self.connection: SocketConnectionWrapper = None
        self.connected = False

    def connect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        LOGGER.info(f'Connecting to {self.anon_host}')
        connection.connect(self.server_addr)
        self.connection = SocketConnectionWrapper(connection)

        self.connection.send_json(self.credentials)
        response = self.connection.recv_json()
        LOGGER.info(f"Connection server response {response}")
        self.connection.token = response.get(LoginArgs.Token)

        while not self.connection.recv_json().get('ready'):
            time.sleep(0.1)
        LOGGER.info('Player thread is ready')

    def disconnect(self):
        try:
            # LOGGER.info(f'Disconnecting')
            self.connection.close()
        except Exception as e:
            LOGGER.error('Failed to disconnect')
            LOGGER.error(e)
        finally:
            self.connected = False
            self.connection = None

    def __del__(self):
        if self.connection:
            self.disconnect()


if __name__ == '__main__':
    connection = SocketConnectionNetwork()
    connection.connect()
    i = 0
    while connection.connection.alive:
        i += 1
        data = {'a': i}
        LOGGER.info(f'DATA: {data}')
        connection.connection.send_json(data)
        time.sleep(0.01)
