from global_obj.main import Global
from core.world.base.map_save import MapSave
from game_client.game_match.stages.abs import Processor
from game_client.game_match.stages.match_menu.UI import GameMatch
from server_stuff.constants.setup_stage import SetupStgConst as SSC


# TODO
class MatchStage(Processor):

    def __init__(self, game, admin: bool):
        super(MatchStage, self).__init__(admin=admin)
        self.game = game
        self.UI: GameMatch = GameMatch(self)

    def process_req(self, r: dict):
        Global.logger.info(f'Match processing: {r}')

    def update(self):
        self.UI.update()

    def connect(self, response: dict):
        Global.logger.info(f'Connecting to match: {response}')
        map_data = response[SSC.Server.StartMatch][SSC.Server.MatchArgs.Map]
        self.UI.w.build_map_from_save(MapSave.get_save_from_dict(map_data))
        self.UI.w.adapt_scale_to_win_size()
        self.UI.define_map_position()

