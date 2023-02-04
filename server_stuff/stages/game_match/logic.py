from global_obj.main import Global
from core.player import Player
from server_stuff.stages.abs import LogicStageAbs
from game_client.server_interactions.network.socket_connection import ConnectionWrapperAbs
from core.world.base.logic.world import LogicWorld
from core.world.base.map_save import MapSave

from server_stuff.constants.common import CommonConst


# TODO
class GameMatch(LogicStageAbs):
    def __init__(self, game_server, server, current_map: MapSave):
        super(GameMatch, self).__init__(game_server, server)
        self.w = LogicWorld()
        self.w.build_map(current_map.flat, current_map.odd, current_map.get_tiles_data())
        self.actions = {
            CommonConst.Chat: self.chat,
        }

    def update(self):
        pass

    def process_request(self, request: dict, connection: ConnectionWrapperAbs, player_obj: Player):
        for action, adata in request.items():
            self.actions.get(action, self.bad_action)(action=action,
                                                      request=request,
                                                      connection=connection,
                                                      player_obj=player_obj)

    def bad_action(self, action: str, player_obj: Player, **kwargs):
        Global.logger.warning(f'Bad request from {player_obj.token} with action "{action}"')

    def chat(self, request: dict, player_obj: Player, **kwargs):
        msg = request.get(CommonConst.Chat, '')
        Global.logger.info(f'{player_obj.token} send a message {msg}')
        if msg:
            self.game_server.send_to_all({CommonConst.Chat: f'{player_obj.nickname}: {msg}'})

    def connect(self, response: dict, connection: ConnectionWrapperAbs):
        pass
