from typing import Callable, Dict
from global_obj.main import Global
from core.world.base.map_save import MapSave
from game_client.game_match.stages.abs import Processor
from game_client.game_match.stages.match_menu.UI import GameMatch
from server_stuff.constants.common import CommonConst
from server_stuff.constants.setup_stage import SetupStgConst as SSC
from core.player.player import Player
from core.mech.base.mech import BaseMech


# TODO
class MatchStage(Processor):

    def __init__(self, game, admin: bool):
        super(MatchStage, self).__init__(admin=admin)
        self.game = game
        self.player: Player = game.player

        self.UI: GameMatch = GameMatch(self)
        self.actions: Dict[str, Callable] = {
            CommonConst.Chat: self.process_player_msg,
        }

    def update(self):
        self.UI.update()

    def process_req(self, r: dict):
        for k in r.keys():
            self.actions.get(k, self.bad_request)(r)

    def bad_request(self, r: dict):
        Global.logger.warning(f'Bad request: {r}')

    def connect(self, response: dict):
        Global.logger.debug(f'Connecting to match: {response}')
        map_data = response[SSC.Server.StartMatch][SSC.Server.MatchArgs.Map]
        Global.details_pool.load_details_list(response[SSC.Server.StartMatch][SSC.Server.MatchArgs.DetailsPool])

        self.UI.w.build_map_from_save(MapSave.get_save_from_dict(map_data))
        self.UI.w.adapt_scale_to_win_size()
        self.UI.define_map_position()

    def process_player_msg(self, r: dict):
        self.UI.chat.add_msg(r[CommonConst.Chat])

    @property
    def mech(self) -> BaseMech:
        return self.player.mech
