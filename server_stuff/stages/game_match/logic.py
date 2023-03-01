import time
from global_obj.main import Global
from core.player.player import Player
from core.world.base.map_save import MapSave
from core.world.base.logic.world import LogicWorld
from server_stuff.stages.abs import LogicStageAbs
from game_client.server_interactions.network.socket_connection import ConnectionWrapperAbs
from server_stuff.constants.game_stage import GameStgConst as GSC

from server_stuff.constants.common import CommonConst
from server_stuff.constants.stages import ServerStages
from core.mech.details.names import DetailNames

from server_stuff.stages.game_match.components.ready import ReadyLogic


class GameMatch(LogicStageAbs, ReadyLogic):
    def __init__(self, game_server, server, current_map: MapSave):
        super(GameMatch, self).__init__(game_server, server)
        self.w = LogicWorld()
        self.w.build_map(current_map.flat, current_map.odd, current_map.get_tiles_data())
        self.players_objs = Global.players_data.players_objs
        self.actions = {
            CommonConst.Chat: self.chat,
            GSC.Time: self.get_time,
        }
        self.last_update = time.time()
        self.time_sync = 0
        self.fill_default_details()

        ReadyLogic.__init__(self)

    def fill_default_details(self):
        for player in self.players_objs.values():
            mech = player.mech
            body = Global.details_pool.add_detail_to_pool(DetailNames.SimpleMetal.Body)
            mech.set_body(body)

            left_arm = Global.details_pool.add_detail_to_pool(DetailNames.SimpleMetal.Arm)
            mech.set_left_detail(0, left_arm)
            right_arm = Global.details_pool.add_detail_to_pool(DetailNames.SimpleMetal.Arm)
            mech.set_right_detail(0, right_arm)

            left_leg = Global.details_pool.add_detail_to_pool(DetailNames.SimpleMetal.Leg)
            mech.set_left_detail(1, left_leg)
            right_leg = Global.details_pool.add_detail_to_pool(DetailNames.SimpleMetal.Leg)
            mech.set_right_detail(1, right_leg)

    def update(self):
        Global.round_clock.update(time.time() - self.last_update)
        self.last_update = time.time()
        self.sync_time()

    def sync_time(self):
        t = int(Global.round_clock.time)
        if t % 1 == 0 and self.time_sync != t:
            self.game_server.send_to_all({GSC.Time: Global.round_clock.time})
            self.time_sync = t

    def process_request(self, request: dict, connection: ConnectionWrapperAbs, player_obj: Player):
        for action in request.keys():
            self.actions.get(action, self.bad_action)(action=action,
                                                      request=request,
                                                      connection=connection,
                                                      player_obj=player_obj)

    def get_time(self, connection: ConnectionWrapperAbs, **kwargs):
        connection.send_json({GSC.Time: Global.round_clock.time})

    def bad_action(self, action: str, player_obj: Player, **kwargs):
        Global.logger.warning(f'Bad request from {player_obj.token} with action "{action}"')

    def chat(self, request: dict, player_obj: Player, **kwargs):
        msg = request.get(CommonConst.Chat, '')
        Global.logger.info(f'{player_obj.token} send a message {msg}')
        if msg:
            self.game_server.send_to_all({CommonConst.Chat: f'{player_obj.nickname}: {msg}'})

    def connect(self, response: dict, connection: ConnectionWrapperAbs):
        response.update(self.get_connection_dict())
        response[ServerStages.SERVER_STAGE] = ServerStages.Game

    def get_connection_dict(self) -> dict:
        conn_d = {
            GSC.MatchData: {
                GSC.MatchArgs.Map: self.game_server.current_map.get_save_dict(),
                GSC.MatchArgs.DetailsPool: Global.details_pool.get_dict(),
                GSC.MatchArgs.PlayersData: self.game_server.get_dict_players_data(),
                GSC.Time: Global.round_clock.time,
            },
        }

        conn_d.update(self.get_ready_players_num_response())

        return conn_d
