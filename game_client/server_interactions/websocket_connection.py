import json
from typing import Any
from abc import abstractmethod
from websocket import WebSocket
from global_obj.logger import get_logger

LOGGER = get_logger()


class ConnectionWrapperAbs:
    alive: bool
    connection: Any

    @abstractmethod
    def recv_json(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def send_json(self, data: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def recv_text(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def send_text(self, data: dict) -> None:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError

    def __del__(self):
        try:
            self.close()
        except:
            pass


class WebSocketConnection(ConnectionWrapperAbs):

    def __init__(self, addr: str = None):
        self.addr: str = addr
        self.alive: bool = True
        self.connection: WebSocket = None
        if addr:
            self.connect(addr)

    def connect(self, addr: str):
        self.addr = addr
        self.connection = WebSocket()
        self.connection.connect(addr)

    def recv_json(self) -> dict:
        j = json.loads(self.recv_text())
        LOGGER.debug(f'Received json: {j}')
        return j

    def send_json(self, data: dict) -> None:
        j = json.dumps(data)
        self.send_text(j)
        LOGGER.info(f'Sending json: {j}')

    def recv_text(self) -> str:
        text = self.connection.recv()
        LOGGER.info(f"Received text: {text}")
        return text

    def send_text(self, data: str) -> None:
        LOGGER.debug(f"Sending text: {data}")
        self.connection.send(data)

    def close(self) -> None:
        if self.connection:
            self.connection.close()
        self.connection = None


if __name__ == '__main__':
    a = WebSocketConnection()
    a.connect('ws://localhost:8000')
    print(a.connection.headers)
