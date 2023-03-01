from core.player.player import Player
from server_stuff.constants.game_stage import GameStgConst as GSC
from game_client.server_interactions.network.socket_connection import ConnectionWrapperAbs


class ReadyLogic:
    actions: dict

    def __init__(self):
        self.actions[GSC.Player.ReadyStatus] = self.set_ready

    def set_ready(self, connection: ConnectionWrapperAbs, player_obj: Player, request: dict, **kwargs):
        if request[GSC.Player.ReadyStatus]:
            if not player_obj.ready:
                self.game_data.players_ready += 1
                player_obj.ready = True
        else:
            if player_obj.ready:
                self.game_data.players_ready -= 1
                player_obj.ready = False

        connection.send_json({GSC.Player.ReadyStatus: player_obj.ready})
        self.send_ready_players_num()

    def send_ready_players_num(self):
        self.game_server.send_to_all(self.get_ready_players_num_response())

    def get_ready_players_num_response(self):
        string = f"{self.game_data.players_ready}/{self.game_data.players_num}"
        return {GSC.ReadyPlayersNumber: string}