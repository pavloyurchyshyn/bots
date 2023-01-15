from typing import Callable, Dict
from global_obj.main import Global
from game_client.game_match.stages.setup_menu.UI import SetupMenu
from game_client.game_match.stages.abs import Processor
from server_stuff.constants.start_and_connect import LoginArgs
from core.world.maps_manager import MapsManager
from server_stuff.constants.setup_stage import SetupStgConst as SSC


class SetupStage(Processor):
    def __init__(self, game, r: dict):
        super(SetupStage, self).__init__(r[LoginArgs.IsAdmin])
        self.exception = None
        self.game = game
        self.maps_mngr: MapsManager = MapsManager()
        self.UI: SetupMenu = SetupMenu(self)
        self.actions: Dict[str, Callable] = {
            SSC.Server.ChosenMap: self.chosen_map,

        }

        self.connect(r)

    def process_req(self, r: dict):
        for k in r.keys():
            self.actions.get(k, self.bad_request)(r)

    def bad_request(self, r: dict):
        Global.logger.warning(f'Bad request: {r}')
        self

    def update(self):
        self.UI.update()
        if self.exception:
            raise self.exception

    def connect(self, response):
        self.UI.maps_mngr.load_from_dict(response[SSC.Maps])
        self.UI.fill_container()
        self.UI.update_chosen_map(response[SSC.Server.ChosenMap])

    def chosen_map(self, r: dict):
        self.UI.update_chosen_map(r.get(SSC.Server.ChosenMap, self.UI.current_save))
