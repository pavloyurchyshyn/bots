import os
import traceback

os.environ['VisualPygameOn'] = 'off'
import _thread
import uvicorn
import asyncio
from typing import Dict

from fastapi import FastAPI, WebSocket
from global_obj.main import Global
from server_stuff.player_client import Client
from server_stuff.abs.server import ServerAbc
from server_stuff.server_login import ServerConnect
from server_stuff.server_config import ServerConfig
from server_stuff.server_game_proxy.main import ServerGameProxy
from server_stuff.constants.requests import CommonReqConst
from server_stuff.constants.start_and_connect import LoginArgs


class PlayerToken(str):
    pass


class GameServer(FastAPI, ServerConnect, ServerAbc):
    def __init__(self):
        super(GameServer, self).__init__()
        ServerConnect.__init__(self)
        self.config: ServerConfig = ServerConfig()
        self.alive_connections: Dict[PlayerToken, Client] = {}
        self.game: ServerGameProxy = ServerGameProxy(self)
        self.server_alive: bool = True

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        if not self.server_alive:
            return

        status, client = await self.process_auth(websocket)

        response = {LoginArgs.Result.Status: status}
        if status == LoginArgs.Result.Connected:
            self.alive_connections[client.token] = client
            self.game.connect(response, client)
            response[LoginArgs.ClientAttrs.ClientData] = client.dict()
            await websocket.send_json(response)

        else:
            await websocket.send_json(response)
            return

        # TODO process connection
        self.notify_about_new_connection(client)
        self.send_updated_connection_list()
        self.send_player_slots()
        await self.handle_client_thread(client)

    def send_player_slots(self):
        self.sync_broadcast(self.game.get_players_slots_dict())

    def send_updated_connection_list(self):
        self.sync_broadcast(self.game.get_connected_players_dict())

    def notify_about_new_connection(self, client: Client):
        self.sync_broadcast({CommonReqConst.Chat: f'{client.nickname} connected.'})

    def sync_broadcast(self, data: dict):
        asyncio.create_task(self.broadcast(data))

    def sync_send_to_client(self, client: Client, data: dict):
        asyncio.create_task(self.send_to_client(client, data))

    async def handle_client_thread(self, client: Client):
        Global.logger.info(f'Started thread for {client.token} {client.nickname}')
        try:
            while self.server_alive and client.alive:
                data = await client.socket.receive_json()
                self.game.process_player_request(client, data)
        except Exception as e:
            Global.logger.error(f'{Client.token} got error\n{e}')
            Global.logger.error(traceback.format_exc())
            await self.disconnect_client(client)
            await self.broadcast({CommonReqConst.Chat: f'{client.nickname} disconnected.'})
            self.send_updated_connection_list()

    async def broadcast(self, data: dict) -> None:
        for client in self.alive_connections.copy().values():
            await self.send_to_client(client=client, data=data)

    async def send_to_client(self, client: Client, data: dict):
        try:
            await client.socket.send_json(data)
        except Exception as e:
            Global.logger.info(f'Failed send to {client.token} because of: {e}')
            Global.logger.info(f'Disconnecting {client.token}')
            await self.disconnect_client(client)

    def sync_disconnect_client(self, client: Client):
        asyncio.create_task(self.disconnect_client(client))

    async def disconnect_client(self, client: Client):
        client.alive = False
        self.alive_connections.pop(client.token, None)
        try:
            await client.socket.close()
        except:
            pass

    def stop(self):
        self.server_alive = False


def main():
    app = GameServer()
    app.add_api_websocket_route('/', app.connect)
    config = uvicorn.Config(app, port=app.config.port)
    server = uvicorn.Server(config)
    _thread.start_new_thread(server.run, ())
    app.game.run()


if __name__ == '__main__':
    try:
        Global.logger.error("Start")
        main()
    except Exception as e:
        Global.logger.error(e)
        Global.logger.error(traceback.format_exc())
        Global.logger.error('Game closed by error')
        exit(1)
