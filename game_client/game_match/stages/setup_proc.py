from typing import Callable, Dict
from global_obj.main import Global
from core.world.maps_manager import MapsManager
from game_client.game_match.stages.abs import Processor
from game_client.game_match.stages.setup_menu.UI import SetupMenu
from server_stuff.constants.common import CommonConst
from server_stuff.constants.setup_stage import SetupStgConst as SSC


class SetupStage(Processor):
    def __init__(self, game, admin: bool):
        super(SetupStage, self).__init__(admin=admin)
        self.exception = None
        self.game = game
        self.maps_mngr: MapsManager = MapsManager()
        self.UI: SetupMenu = SetupMenu(self)
        self.actions: Dict[str, Callable] = {
            SSC.Server.ChosenMap: self.chosen_map,
            SSC.Server.StartMatch: self.start_game,
            CommonConst.Chat: self.process_player_msg,
        }

    def process_req(self, r: dict):
        for k in r.keys():
            self.actions.get(k, self.bad_request)(r)

    def bad_request(self, r: dict):
        Global.logger.warning(f'Bad request: {r}')

    def update(self):
        self.UI.update()
        if self.exception:
            raise self.exception

    def connect(self, response: dict):
        self.UI.maps_mngr.load_from_dict(response[SSC.Maps])
        self.UI.fill_container()
        self.chosen_map(response)

    def chosen_map(self, r: dict):
        self.UI.update_chosen_map(r.get(SSC.Server.ChosenMap, self.UI.current_save), force=True)

    def start_game(self, r: dict):
        self.game.connect_to_game(r)

    def process_player_msg(self, r: dict):
        self.UI.chat.add_msg(r[CommonConst.Chat])