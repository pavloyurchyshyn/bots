from typing import Callable, Dict
from global_obj.main import Global
from core.player.player import PlayerObj
from core.mech.base.mech import BaseMech
from core.world.base.map_save import MapSave
from game_client.game_match.stages.abs import Processor
from game_client.game_match.stages.match_menu.UI import GameMatch
from core.player.constants import PlayerAttrs
from server_stuff.constants.requests import GameStgConst as GSC
from server_stuff.constants.requests import CommonReqConst, GameStgConst

from game_logic.game_data.game_settings import GameSettings
from game_logic.game import Game

from game_client.game_match.stages.match_menu.proc_components.ready import ReadyProc
from game_client.game_match.stages.match_menu.proc_components.cards import CardsProc


class MatchStage(Processor):  # , ReadyProc, CardsProc):
    def __init__(self, stages_controller, admin: bool):
        super(MatchStage, self).__init__(admin=admin)
        self.stages_controller = stages_controller
        self.game_object: Game = None
        self.settings: GameSettings = None
        self.UI: GameMatch = None
        self.actions: Dict[str, Callable] = {
            CommonReqConst.Chat: self.process_player_msg,
        }

        # ReadyProc.__init__(self)
        # CardsProc.__init__(self)

    def update(self):
        self.UI.update()

    def process_request(self, r: dict, **kwargs):
        for k in r.keys():
            self.actions.get(k, self.bad_request)(r)

    def bad_request(self, r: dict):
        Global.logger.warning(f'Bad request: {r}')

    def connect(self, response: dict):
        Global.logger.info(f'Connecting to match: {response}')
        # match_data = response[GSC.MatchData]
        self.settings: GameSettings = GameSettings(players_num=response[GameStgConst.Settings].pop('players_num', 0),
                                                   real_players_num=response[GameStgConst.Settings].pop(
                                                       'real_players_num', 0),
                                                   **response[GameStgConst.Settings])
        save = MapSave.get_save_from_dict(response[GameStgConst.Map])
        self.UI = GameMatch(self)
        self.UI.w.build_map(save.flat, save.odd, save.get_tiles_data())

        players_data = response[GameStgConst.PlayersData]

        self.game_object: Game = Game(world=self.UI.w, setting=self.settings,
                                      players={}, bots=[])
        Global.set_game_obj(self.game_object)
        players = {int(slot): PlayerObj.get_player_from_dict(player_data)
                   for slot, player_data
                   in players_data.items()}
        self.game_object.players = players
        print('=' * 20)
        print(players_data)

        print(players)
        print('=' * 20)
        # Global.details_pool.load_details_list(match_data[GSC.MatchArgs.DetailsPool])
        # self.update_time(match_data)
        # self.update_players_ready_number(response)

        # self.UI.w.build_map_from_save(MapSave.get_save_from_dict(match_data[GSC.Map]))
        # self.UI.w.adapt_scale_to_win_size()
        # self.UI.define_map_position()
        # self.UI.collect_skills_deck()

    def process_player_msg(self, r: dict):
        self.UI.chat.add_msg(r[CommonReqConst.Chat])
