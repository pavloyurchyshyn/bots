import asyncio
from typing import Tuple, Dict, Optional
from fastapi import WebSocket
from server_stuff.player_client import Client
from core.player.constants import PlayerAttrs
from server_stuff.constants.start_and_connect import LoginArgs
from server_stuff.server_config import ServerConfig


class ServerConnect:
    config: ServerConfig
    token_player_link: Dict[str, int]
    alive_connections: Dict[str, Client] = {}

    async def process_auth(self, socket: WebSocket) -> Tuple[str, Optional[Client]]:
        data = await socket.receive_json()

        password = data[LoginArgs.Password]
        old_token = data[LoginArgs.Token]
        nickname = data[LoginArgs.ClientAttrs.NickName]
        client = Client(nickname=nickname,
                        socket=socket,
                        player_number=1,
                        is_admin=self.is_player_admin(old_token),
                        )

        return LoginArgs.Result.Connected, client

    def success_connection(self, password, old_token, nickname):
        # TODO return result and client
        pass

    def is_player_admin(self, token: str) -> bool:
        return True  # TODO delete
        return self.config.admin_token == token
