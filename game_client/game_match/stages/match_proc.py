from typing import Callable, Dict
from global_obj.main import Global
from core.player.player import Player
from core.mech.base.mech import BaseMech
from core.world.base.map_save import MapSave
from game_client.game_match.stages.abs import Processor
from game_client.game_match.stages.match_menu.UI import GameMatch
from server_stuff.constants.common import CommonConst
from server_stuff.constants.game_stage import GameStgConst as GSC
from core.player.constants import PlayerAttrs


class MatchStage(Processor):

    def __init__(self, game, admin: bool):
        super(MatchStage, self).__init__(admin=admin)
        self.game = game
        self.player: Player = game.player

        self.UI: GameMatch = GameMatch(self)
        self.actions: Dict[str, Callable] = {
            CommonConst.Chat: self.process_player_msg,
            GSC.Time: self.update_time,
        }

    def update(self):
        self.UI.update()

    def process_req(self, r: dict):
        for k in r.keys():
            self.actions.get(k, self.bad_request)(r)

    def update_time(self, r: dict):
        Global.logger.debug(f'Updated time: {r[GSC.Time]}')
        Global.round_clock.set_time(r[GSC.Time])

    def bad_request(self, r: dict):
        Global.logger.warning(f'Bad request: {r}')

    def connect(self, response: dict):
        Global.logger.debug(f'Connecting to match: {response}')
        match_data = response[GSC.MatchData]
        Global.details_pool.load_details_list(match_data[GSC.MatchArgs.DetailsPool])
        self.update_players(match_data[GSC.MatchArgs.PlayersData])
        self.update_time(match_data)

        self.UI.w.build_map_from_save(MapSave.get_save_from_dict(match_data[GSC.MatchArgs.Map]))
        self.UI.w.adapt_scale_to_win_size()
        self.UI.define_map_position()
        self.UI.collect_skills_deck()

    def update_players(self, players_data: dict):
        for token, data in players_data.items():
            if token == self.player.token:
                Global.logger.warning(f'Updating this player: {data}')
                mech = data.pop(PlayerAttrs.Mech)
                self.player.update_attrs(data)
                self.player.mech = Global.mech_serializer.dict_to_mech(mech)
            elif token in Global.players_data.players_objs:
                Global.logger.info(f'Updating player: {data}')
                Global.players_data.players_objs[token].update_attrs(data)
            else:
                Global.logger.warning(f'Creating new player: {data}')
                Global.players_data.players_objs[token] = Player.get_player_from_dict(data)

    def process_player_msg(self, r: dict):
        self.UI.chat.add_msg(r[CommonConst.Chat])

    @property
    def mech(self) -> BaseMech:
        return self.player.mech
