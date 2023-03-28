from global_obj.main import Global
from server_stuff.constants.requests import GameStgConst as GSC


class ReadyProc:
    actions: dict

    def __init__(self):
        self.actions[GSC.Time] = self.update_time
        self.actions[GSC.Player.ReadyStatus] = self.update_ready_status
        self.actions[GSC.ReadyPlayersNumber] = self.update_players_ready_number

    def update_time(self, r: dict):
        Global.logger.debug(f'Updated time: {r[GSC.Time]}')
        Global.round_clock.set_time(r[GSC.Time])

    def update_ready_status(self, r: dict):
        Global.logger.info(f'Ready status: {r[GSC.Player.ReadyStatus]}')
        self.player.ready = r[GSC.Player.ReadyStatus]
        self.UI.ready_win.change_button_color_to_ready()

    def update_players_ready_number(self, r: dict):
        Global.logger.info(f"Ready players {r[GSC.ReadyPlayersNumber]}")
        self.UI.ready_win.set_ready_players_text(r[GSC.ReadyPlayersNumber])

