import json
import socket
from abc import abstractmethod, ABC


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
        raise NotImplementedError

    def __del__(self):
        try:
            self.close()
        except:
            pass


class SocketConnection(ConnectionWrapperAbs):
    START_OF_REQUEST = b'\x00\x00\x00'
    END_OF_REQUEST = b'\x00\x00'

    def __init__(self, logger, family=socket.AF_INET, type_=socket.SOCK_STREAM):
        self.connection: socket.socket = None
        self.family = family
        self.type = type_
        self.alive = False
        self.logger = logger

    def connect(self, addr: str):
        self.connection: socket.socket = socket.socket(self.family, self.type)
        self.connection.connect(addr)
        self.alive = True

    def set_connection(self, connection: socket.socket) -> 'SocketConnection':
        self.connection = connection
        self.alive = True
        return self

    def recv_json(self, size=2048) -> dict:
        return self.recv_to_json(self.recv(size=size))

    def recv(self, size=2048) -> bytes:
        recv = b''
        while not recv.endswith(SocketConnection.END_OF_REQUEST):
            recv += self.recv_from_connection(self.connection, size)
        self.logger.debug(f'Received: {recv}')
        return recv

    @staticmethod
    def recv_to_json(data: bytes) -> dict:
        recv = data.split(SocketConnection.START_OF_REQUEST)[-1]
        recv = recv.replace(SocketConnection.END_OF_REQUEST, b'')
        recv = recv.decode()

        if recv == '{}':
            return {}

        return json.loads(recv)

    def send_json(self, data: dict) -> None:

        try:
            self.send(SocketConnection.START_OF_REQUEST
                      + json.dumps(data).encode()
                      + SocketConnection.END_OF_REQUEST)
        except Exception as e:
            self.logger.critical(e)
            self.close()

    def change_connection(self, connection: socket):
        self.connection: socket = connection

    def send(self, data: bytes):
        self.logger.debug(f'Sending: {data}')

        self.connection.send(data)

    @staticmethod
    def recv_from_connection(connection, size=2048) -> bytes:
        return connection.recv(size)

    def close(self):
        self.alive = False
        if self.connection:
            try:
                self.connection.close()
            except Exception as e:
                self.logger.error(f'Failed to disconnect: {e}')
            else:
                self.logger.info(f'Successfully disconnected!')
        self.connection = None

