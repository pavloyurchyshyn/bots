import json
from socket import socket
from abc import abstractmethod, ABC

from global_obj.logger import get_logger


LOGGER = get_logger()


class ConnectionAbs(ABC):
    @abstractmethod
    def send(self, data: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def recv(self, size: int = 2048) -> dict:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError


class ConnectionWrapperAbs:
    alive: bool
    connection: ConnectionAbs
    token: str

    @abstractmethod
    def recv_json(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def send_json(self, data: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def change_connection(self, connection: ConnectionAbs):
        raise NotImplementedError

    def send(self, data: bytes) -> None:
        raise NotImplementedError

    def recv(self, size=2048) -> bytes:
        raise NotImplementedError

    def close(self) -> None:
        try:
            self.connection.close()
        except Exception as e:
            LOGGER.error(f'Failed to disconnect {self.token}: {e}')
        else:
            LOGGER.info(f'{self.token} disconnected!')

    def __del__(self):
        try:
            self.close()
        except:
            pass


class SocketConnectionWrapper(ConnectionWrapperAbs):
    START_OF_REQUEST = b'\x00\x00\x00'
    END_OF_REQUEST = b'\x00\x00'

    def __init__(self, connection: socket, token: str = None):
        self.connection: socket = connection
        self.token = token
        self.alive = True

    def recv_json(self, size=2048) -> dict:
        return self.recv_to_json(self.recv(size=2048))

    def recv(self, size=2048) -> bytes:
        recv = b''
        while not recv.endswith(SocketConnectionWrapper.END_OF_REQUEST):
            recv += self.recv_from_connection(self.connection, size)
        return recv

    @staticmethod
    def recv_to_json(data: bytes) -> dict:
        recv = data.split(SocketConnectionWrapper.START_OF_REQUEST)[-1]
        recv = recv.replace(SocketConnectionWrapper.END_OF_REQUEST, b'')
        recv = recv.decode()

        if recv == '{}':
            return {}

        return json.loads(recv)

    def send_json(self, data: dict) -> None:
        try:
            self.send(SocketConnectionWrapper.START_OF_REQUEST + json.dumps(
                data).encode() + SocketConnectionWrapper.END_OF_REQUEST)
        except Exception as e:
            LOGGER.critical(e)
            self.close()

    def change_connection(self, connection: socket):
        self.connection: socket = connection

    def send(self, data: bytes):
        self.connection.send(data)

    @staticmethod
    def recv_from_connection(connection, size=2048) -> bytes:
        return connection.recv(size)

    def close(self):
        if self.connection:
            try:
                self.connection.close()

            except Exception as e:
                LOGGER.error(f'Failed to disconnect {self.token}: {e}')
            else:
                LOGGER.info(f'{self.token} disconnected!')
        self.alive = False
        self.connection = None

    def __del__(self):
        try:
            self.close()
        except:
            pass


if __name__ == '__main__':
    data = {'a': 1}
    r = SocketConnectionWrapper.START_OF_REQUEST + json.dumps(data).encode() + SocketConnectionWrapper.END_OF_REQUEST
    print(r)
