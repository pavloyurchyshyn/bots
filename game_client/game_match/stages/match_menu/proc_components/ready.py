from global_obj.main import Global
from server_stuff.constants.requests import GameStgConst as GSC
from core.player.player import PlayerObj
from game_client.game_match.stages.match_menu.UI import GameMatch


class ReadyProc:
    actions: dict
    UI: GameMatch
    player: PlayerObj

    def __init__(self):
        self.actions[GSC.Time] = self.update_time
        self.actions[GSC.Player.ReadyStatus] = self.update_ready_status
        self.actions[GSC.ReadyPlayersNumber] = self.update_players_ready_number

    def update_time(self, r: dict, request_data=None, **kwargs):
        Global.logger.debug(f'Updated time: {r[GSC.Time]}')
        Global.round_clock.set_time(r[GSC.Time])

    def update_ready_status(self, r: dict, request_data, **kwargs):
        Global.logger.debug(f'Ready status: {request_data}')
        self.player.ready = request_data
        self.UI.ready_win.change_button_color_to_ready()

    def update_players_ready_number(self, r: dict, request_data, **kwargs):
        Global.logger.debug(f"Ready players {request_data}")
        self.UI.ready_win.set_ready_players_text(request_data)

