from typing import Callable, Dict

from global_obj.main import Global

from core.player.player import PlayerObj
from core.mech.mech import BaseMech
from core.world.base.map_save import MapSave

from game_client.game_match.stages.abs import Processor
from game_client.game_match.stages.match_menu.UI import GameMatch

from server_stuff.constants.requests import CommonReqConst, GameStgConst

from game_logic.game import Game
from game_logic.game_data.game_settings import GameSettings

from game_client.game_match.stages.match_menu.proc_components.ready import ReadyProc


class MatchStage(Processor, ReadyProc):  # , CardsProc):
    def __init__(self, stages_controller):
        self.stages_controller = stages_controller
        self.game_object: Game = None
        self.settings: GameSettings = None
        self.UI: GameMatch = None
        self.actions: Dict[str, Callable] = {
            CommonReqConst.Chat: self.process_player_msg,
        }

        ReadyProc.__init__(self)
        # CardsProc.__init__(self)

    @property
    def player(self) -> PlayerObj:
        return self.game_object.players[Global.network_data.slot]

    @property
    def mech(self) -> BaseMech:
        return self.player.mech

    def update(self):
        self.UI.update()

    def process_request(self, r: dict):
        for k in r.keys():
            self.actions.get(k, self.bad_request)(r, request_data=r[k])

    def bad_request(self, r: dict, request_data, **_):
        Global.logger.warning(f'Bad request: {r}:\n{request_data}')

    def connect(self, response: dict):
        Global.logger.info(f'Connecting to match: {response}')
        settings = response[GameStgConst.Settings]
        self.settings: GameSettings = GameSettings(players_num=settings.pop('players_num', 0),
                                                   real_players_num=settings.pop('real_players_num', 0),
                                                   **response[GameStgConst.Settings])
        save = MapSave.get_save_from_dict(response[GameStgConst.Map])
        self.UI: GameMatch = GameMatch(self)
        self.UI.w.build_map(save.flat, save.odd, save.get_tiles_data())
        self.UI.w.adapt_scale_to_win_size()
        self.UI.define_map_position()

        self.game_object: Game = Game(world=self.UI.w, setting=self.settings,
                                      players={}, bots=[])
        Global.set_game_obj(self.game_object)

        Global.logger.info(f'Loading pool: {response[GameStgConst.DetailsPool]}')
        Global.details_pool.load_details_classes_list(response[GameStgConst.DetailsPool])

        players_data = response[GameStgConst.PlayersData]
        Global.logger.info(f'Loading players: {players_data}')
        players = {int(slot): PlayerObj.get_player_from_dict(player_data)
                   for slot, player_data
                   in players_data.items()}
        self.game_object.players = players

        # Global.details_pool.load_details_list(match_data[GSC.MatchArgs.DetailsPool])
        self.update_time(response, response[GameStgConst.Time])
        # self.update_players_ready_number(response)

        # self.UI.w.build_map_from_save(MapSave.get_save_from_dict(match_data[GSC.Map]))
        # self.UI.w.adapt_scale_to_win_size()
        # self.UI.define_map_position()
        self.UI.collect_skills_deck()

    def process_player_msg(self, r: dict, request_data, **kwargs):
        self.UI.chat.add_msg(request_data)
