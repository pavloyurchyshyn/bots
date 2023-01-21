from global_obj.main import Global
from server_stuff.stages.abs import LogicStageAbs
from server_stuff.constants.stages import ServerStages
from game_client.server_interactions.network.socket_connection import ConnectionWrapperAbs
from core.world.maps_manager import MapsManager
from server_stuff.constants.setup_stage import SetupStgConst as SSC

from core.player import Player
from server_stuff.constants.common import CommonConst


class GameSetup(LogicStageAbs):

    def __init__(self, game_server, server):
        self.actions = {
            CommonConst.Chat: self.chat,
            SSC.Player.ChooseMap: self.choose_map,
            SSC.Player.StartMatch: self.start_match,
        }
        super().__init__(game_server, server)
        self.maps_mngr: MapsManager = game_server.maps_mngr
        self.players_objs = game_server.players_objs
        self.chosen_map: int = 0

    def update(self):
        pass

    def process_request(self, request: dict, connection: ConnectionWrapperAbs, player_obj: Player):
        for action, adata in request.items():
            self.actions.get(action, self.bad_action)(action=action,
                                                      request=request,
                                                      connection=connection,
                                                      player_obj=player_obj)

        # response = {'ok': 'process_request ok',
        #             }
        # Global.logger.info(f'Response to {connection.token}: {response}')
        # connection.send_json(response)

    def bad_action(self, action: str, player_obj: Player, **kwargs):
        Global.logger.warning(f'Bad request from {player_obj.token} with action "{action}"')

    def connect(self, response: dict, connection: ConnectionWrapperAbs):
        response[SSC.Maps] = [save.get_save_dict() for save in self.maps_mngr.maps if save]
        response[SSC.Server.ChosenMap] = self.chosen_map

        response[ServerStages.SERVER_STAGE] = ServerStages.GameSetup

    def choose_map(self, request: dict, player_obj: Player, **kwargs):
        Global.logger.info(f'{player_obj.token} changing map.')
        if player_obj.is_admin:
            map__ = map_ = request.get(SSC.Player.ChooseMap, 0)
            try:
                map_ = int(map_)
            except Exception as e:
                Global.logger.error(f'Wrong map format {map__}. Error {e}')
                return
            if map_ == self.chosen_map:
                Global.logger.info(f'This map already chosen')
                return
            if map_ + 1 > len(self.maps_mngr.maps):
                Global.logger.warning(f'Player {player_obj.token} asking for bad map id {map_}')
                return

            # TODO check for maps count
            Global.logger.info(f'{player_obj.token} changing map to {map_}')

            self.game_server.send_to_all({SSC.Server.ChosenMap: map_})
            self.chosen_map = map_
            self.game_server.current_map = self.maps_mngr.maps[self.chosen_map]
            Global.logger.debug('All ok')
        else:
            Global.logger.debug(f'Player {player_obj.token} is not admin!')

    def start_match(self, request: dict, player_obj: Player, **kwargs):
        if player_obj.is_admin:
            if request[SSC.Player.StartMatch] and not self.game_server.started_match:
                Global.logger.info(f'Game data: {request}')
                self.game_server.start_game_match()

        else:
            Global.logger.warning(f'Non admin {player_obj.token} asking for start')

    def chat(self, request: dict, player_obj: Player, **kwargs):
        msg = request.get(CommonConst.Chat, '')
        Global.logger.info(f'{player_obj.token} send a message {msg}')
        if msg:
            self.game_server.send_to_all({CommonConst.Chat: f'{player_obj.nickname}: {msg}'})
