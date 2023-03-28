from typing import Dict
from abc import abstractmethod
from fastapi import WebSocket
from server_stuff.player_client import Client
from server_stuff.server_config import ServerConfig


class PlayerToken(str):
    pass


class ServerAbc:
    alive_connections: Dict[str, Client]
    config: ServerConfig
    server_alive: bool

    @abstractmethod
    async def connect(self, websocket: WebSocket):
        raise NotImplementedError

    @abstractmethod
    async def handle_client_thread(self, client: Client):
        raise NotImplementedError

    @abstractmethod
    async def broadcast(self, data: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def sync_broadcast(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    def sync_send_to_client(self, client: Client, data: dict):
        raise NotImplementedError

    @abstractmethod
    def send_updated_connection_list(self):
        raise NotImplementedError

    @abstractmethod
    async def send_to_client(self, client: Client, data: dict):
        raise NotImplementedError

    @abstractmethod
    def sync_disconnect_client(self, client: Client):
        raise NotImplementedError

    @abstractmethod
    async def disconnect_client(self, client: Client):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError

    @abstractmethod
    def send_player_slots(self):
        raise NotImplementedError
