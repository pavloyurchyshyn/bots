from core.player.player import PlayerObj
from server_stuff.player_client import Client
from server_stuff.constants.requests import GameStgConst as GSC
from server_stuff.server_game_proxy.game_stage.components.abs import ComponentAbs


class ReadyLogic(ComponentAbs):

    def __init__(self):
        self.actions[GSC.Player.ReadyStatus] = self.set_player_ready_status

    def set_player_ready_status(self, request: dict, client: Client, player_obj: PlayerObj, **kwargs):
        player_obj.ready = request[GSC.Player.ReadyStatus]
        self.server.sync_send_to_client(client, {GSC.Player.ReadyStatus: player_obj.ready})
        self.send_ready_players_num()

    def send_ready_players_num(self):
        string = f"{self.game_logic.ready_players_number}/{self.game_logic.players_num}"
        self.server.sync_broadcast({GSC.ReadyPlayersNumber: string})
