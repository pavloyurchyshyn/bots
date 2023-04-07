from typing import Callable, Dict
from global_obj.main import Global
from core.world.maps_manager import MapsManager
from game_client.game_match.stages.abs import Processor
from game_client.game_match.stages.setup_menu.UI import SetupMenu
from server_stuff.constants.requests import CommonReqConst, SetupStageReq as SSR


class SetupStage(Processor):
    def __init__(self, stages_controller):
        self.exception = None
        self.stages_controller = stages_controller
        self.maps_mngr: MapsManager = MapsManager()
        self.UI: SetupMenu = SetupMenu(self)
        self.actions: Dict[str, Callable] = {
            SSR.Server.ChosenMap: self.chosen_map,
            SSR.Server.StartMatch: self.start_game,

            CommonReqConst.Chat: self.process_player_msg,
            CommonReqConst.Disconnect: self.disconnect_me,
            CommonReqConst.PlayersSlots: self.process_players_slots,
            CommonReqConst.ConnectedPlayers: self.update_connected_players,
            CommonReqConst.SendSlotToPlayer: self.get_my_slot,
        }

    def process_request(self, r: dict, **kwargs):
        for k in r.keys():
            self.actions.get(k, self.bad_request)(r)

    def bad_request(self, r: dict):
        Global.logger.warning(f'Bad request: {r}')

    def update(self):
        self.UI.update()
        if self.exception:
            raise self.exception

    def connect(self, response: dict):
        self.UI.maps_mngr.load_from_dict(response[SSR.Maps])
        self.UI.fill_container()
        self.update_connected_players(response)
        self.chosen_map(response)

    def get_my_slot(self, r: dict):
        Global.logger.info(f'My new slot {r[CommonReqConst.SendSlotToPlayer]}')
        Global.network_data.slot = r[CommonReqConst.SendSlotToPlayer]

    def update_connected_players(self, r: dict):
        self.UI.fill_connected(r[CommonReqConst.ConnectedPlayers])

    def chosen_map(self, r: dict):
        self.UI.update_chosen_map(r.get(SSR.Server.ChosenMap, self.UI.current_save), force=True)

    def start_game(self, r: dict):
        self.stages_controller.connect_to_game(r[SSR.Server.StartMatch])

    def process_player_msg(self, r: dict):
        self.UI.chat.add_msg(r[CommonReqConst.Chat])

    def send_start_request(self):
        Global.connection.send_json({SSR.Player.StartMatch: True})

    def disconnect_me(self, r: dict):
        Global.stages.close_game()
        self.stages_controller.alive = False
        self.stages_controller.add_popup_to_mmenu(r[CommonReqConst.Disconnect])

    def process_players_slots(self, r: dict):
        self.UI.fill_players_slots(r[CommonReqConst.PlayersSlots])
