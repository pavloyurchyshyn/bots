import asyncio
from fastapi import WebSocket
from server_stuff.constants.start_and_connect import LoginArgs
from global_obj.logger import get_logger

LOGGER = get_logger()

class Client:
    def __init__(self, nickname: str,
                 socket: WebSocket,
                 player_number: int,
                 is_admin: bool = False,
                 slot: int = None):
        self.alive: bool = True
        self.nickname: str = nickname
        self.socket: WebSocket = socket
        self.is_admin: bool = is_admin
        self.player_number: int = player_number
        self.slot: int = slot

    def sync_send_json(self, data: dict):
        LOGGER.info(f'Send to {str(self)}: {data}')
        asyncio.create_task(self.socket.send_json(data))

    @property
    def token(self):
        return self.socket.headers['sec-websocket-key']

    def dict(self) -> dict:
        return {
            LoginArgs.ClientAttrs.IsAdmin: self.is_admin,
            LoginArgs.ClientAttrs.Number: self.player_number,
            LoginArgs.ClientAttrs.NickName: self.nickname,
            LoginArgs.Token: self.token,
        }

    def __str__(self):
        return f'{self.nickname}<->{self.token[:4]}...'