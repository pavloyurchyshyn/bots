from typing import Dict, List
from global_obj.main import Global
from server_stuff.constants.stages import ServerStages
from server_stuff.constants.requests import SetupStageReq as SSR
from server_stuff.abs.server import ServerAbc
from core.world.base.map_save import MapSave
from game_logic.bots.bot_player import BotPlayer

from server_stuff.player_client import Client
from server_stuff.constants.requests import CommonReqConst, GameStgConst
from game_logic.game import Game
from core.world.base.logic.world import LogicWorld
from game_logic.game_data.game_settings import GameSettings

from core.player.player import PlayerObj


class GameMatch:

    def __init__(self, server_game_proxy, server):
        self.actions = {
            CommonReqConst.Chat: self.chat,
        }
        self.server: ServerAbc = server
        self.server_game_proxy = server_game_proxy
        self.game_obj: Game = None
        self.current_map_save: MapSave = MapSave()

    def connect(self, response: dict, client: Client):
        response.update(self.get_game_dict())

    def get_game_dict(self) -> dict:
        return {
            ServerStages.SERVER_STAGE: ServerStages.Game,
            GameStgConst.Settings: self.game_obj.settings.dict(),
            GameStgConst.Map: self.current_map_save.get_save_dict(),
        }

    def setup(self, map_save: MapSave, settings: GameSettings,
              players: Dict[int, PlayerObj], bots: List[BotPlayer]
              ):
        world = LogicWorld()
        world.build_map(flat=map_save.flat, odd=map_save.odd, data=map_save.get_tiles_data())

        self.current_map_save.set_name(map_save.name)
        self.current_map_save.set_world_to_json_data(world)
        self.game_obj: Game = Game(world=world, setting=settings, players=players, bots=bots)
        Global.set_game_obj(self.game_obj)

    def update(self):
        pass

    def process_request(self, request: dict, client: Client):
        for action, data in request.items():
            self.actions.get(action, self.bad_action)(action=action,
                                                      request=request,
                                                      client=client,
                                                      player_obj=None)

    def bad_action(self, action: str, client: Client, **kwargs):
        Global.logger.warning(f'Bad request from {client.token} with action "{action}"')

    def chat(self, request: dict, client: Client, **kwargs):
        msg = request.get(CommonReqConst.Chat, '')
        Global.logger.info(f'{client.token} send a message {msg}')
        if msg:
            self.server.sync_broadcast({CommonReqConst.Chat: f'{client.nickname}: {msg}'})
