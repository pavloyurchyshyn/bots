from typing import Dict, List
from global_obj.main import Global
from server_stuff.constants.stages import ServerStages
from server_stuff.abs.server import ServerAbc
from core.world.base.map_save import MapSave
from game_logic.bots.bot_player import BotPlayer

from server_stuff.player_client import Client
from server_stuff.constants.requests import CommonReqConst, GameStgConst as GSC
from game_logic.game import Game
from core.world.base.logic.world import LogicWorld
from game_logic.game_data.game_settings import GameSettings

from core.player.player import PlayerObj

from server_stuff.server_game_proxy.game_stage.components.ready import ReadyLogic

from game_logic.game_data.id_generator import IdGenerator
from core.mech.pools.details_pool import DetailsPool


class GameMatch(ReadyLogic):

    def __init__(self, server_game_proxy, server):
        self.actions = {
            CommonReqConst.Chat: self.chat,
        }
        ReadyLogic.__init__(self)

        self.server: ServerAbc = server
        self.server_game_proxy = server_game_proxy
        self.game_logic: Game = None
        self.current_map_save: MapSave = MapSave()

    def connect(self, response: dict, client: Client):
        response.update(self.get_game_dict())

    def get_game_dict(self) -> dict:
        return {
            ServerStages.SERVER_STAGE: ServerStages.Game,
            GSC.Settings: self.game_logic.settings.dict(),
            GSC.Map: self.current_map_save.get_save_dict(),
            GSC.DetailsPool: self.game_logic.details_pool.get_dict(),
            GSC.PlayersData: {k: player.get_dict() for k, player in self.game_logic.players.items()},
            GSC.Time: Global.round_clock.time,
        }

    def setup(self, map_save: MapSave,
              settings: GameSettings,
              players: Dict[int, PlayerObj],
              bots: List[BotPlayer],
              id_generator: IdGenerator,
              details_pool: DetailsPool
              ):
        world = LogicWorld()
        world.build_map(flat=map_save.flat, odd=map_save.odd, data=map_save.get_tiles_data())

        self.current_map_save.set_name(map_save.name)
        self.current_map_save.set_world_to_json_data(world)
        self.game_logic: Game = Game(world=world, setting=settings,
                                     players=players, bots=bots,
                                     id_generator=id_generator,
                                     details_pool=details_pool,
                                     )
        Global.set_game_obj(self.game_logic)

    def update(self):
        pass

    def process_request(self, request: dict, client: Client):
        for action, data in request.items():
            self.actions.get(action, self.bad_action)(action=action,
                                                      request=request,
                                                      client=client,
                                                      player_obj=self.get_player_obj(client))

    def bad_action(self, action: str, request: dict, client: Client, **kwargs):
        Global.logger.warning(f'Bad request from {client.token} with action "{action}: {request[action]}"')

    def chat(self, request: dict, client: Client, **kwargs):
        msg = request.get(CommonReqConst.Chat, '')
        Global.logger.info(f'{client.token} send a message {msg}')
        if msg:
            self.server.sync_broadcast({CommonReqConst.Chat: f'{client.nickname}: {msg}'})

    def get_player_obj(self, client: Client) -> PlayerObj:
        return self.game_logic.players.get(client.slot)