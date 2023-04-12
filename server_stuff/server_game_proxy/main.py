import time
import traceback
from global_obj.main import Global
from core.player.player import PlayerObj
from core.mech.mech import BaseMech
from core.mech.pools.details_pool import DetailsPool


from server_stuff.player_client import Client
from server_stuff.abs.server import ServerAbc
from server_stuff.server_game_proxy.game_stage.main import GameMatch
from server_stuff.server_game_proxy.setup_stage.main import GameSetup
from server_stuff.constants.requests import CommonReqConst, SetupStageReq

from game_logic.bots.bot_player import BotPlayer
from game_logic.settings_stage import SettingsStage
from game_logic.game_data.id_generator import IdGenerator

SERVER_LIVE_TIME = 60


# TODO make abstract
class ServerGameProxy:
    def __init__(self, server):
        self.server: ServerAbc = server
        self.started_match: bool = False

        self.setup_stage: GameSetup = GameSetup(server_game_proxy=self, server=self.server)

        self.current_stage = self.setup_stage

    def run(self):
        a = time.time() + SERVER_LIVE_TIME
        while time.time() < a:
            self.current_stage.update()
            time.sleep(0.1)
        Global.logger.info('end of game')

    def start_game_match(self):
        try:
            Global.logger.info('Start game match')
            id_generator: IdGenerator = IdGenerator()
            details_pool: DetailsPool = DetailsPool(id_generator=id_generator)

            game: GameMatch = GameMatch(server_game_proxy=self, server=self.server)
            players = {}
            bots = []

            real_players_num = 0
            players_num = 0
            for slot, token in self.setup_stage.game_logic.players_slots.items():
                if token is None:
                    continue
                players_num += 1

                if token == self.setup_stage.game_logic.BOT_TOKEN:
                    nickname = f'Bot_{slot}'
                else:
                    nickname = self.server.alive_connections[token].nickname
                    real_players_num += 1

                position = self.setup_logic.current_map.spawns[slot]
                mech: BaseMech = details_pool.get_simple_mech(position=position)
                player_obj = PlayerObj(nickname=nickname,
                                       mech=mech,
                                       spawn=position,
                                       scenario=dict.fromkeys(tuple(range(self.setup_logic.settings.actions_count))),
                                       under_bot_control=token == self.setup_stage.game_logic.BOT_TOKEN,
                                       )
                if token == self.setup_stage.game_logic.BOT_TOKEN:
                    bots.append(BotPlayer(slot=slot, player_obj=player_obj))

                players[slot] = player_obj

            self.setup_logic.settings.real_players_num = real_players_num
            self.setup_logic.settings.players_num = players_num

            game.setup(self.setup_stage.game_logic.current_map,
                       settings=self.setup_logic.settings,
                       players=players,
                       bots=bots,
                       id_generator=id_generator,
                       details_pool=details_pool,
                       )

            self.server.sync_broadcast({SetupStageReq.Server.StartMatch: game.get_game_dict()})

            self.current_stage = game
            self.current_stage.game_logic.players_slots = self.setup_stage.game_logic.players_slots
            game.send_ready_players_num()
            # del self.setup_stage
        except Exception as e:
            Global.logger.error('Failed to start game.')
            Global.logger.error(str(e))
            Global.logger.error(traceback.format_exc())
            # TODO disconnect all

    def send_broadcast_chat(self, msg: str):
        self.server.sync_broadcast({CommonReqConst.Chat: msg})

    def connect(self, response: dict, client: Client):
        self.current_stage.connect(response=response, client=client)
        response.update(self.get_connected_players_dict())

    def process_player_request(self, client: Client, request: dict):
        self.current_stage.process_request(request, client)

    def get_connected_players_dict(self) -> dict:
        clients = {client.token: (self.current_stage.game_logic.players_slots.get(client.token), client.nickname)
                   for client in
                   self.server.alive_connections.values()}
        return {CommonReqConst.ConnectedPlayers: clients}

    def get_players_slots_dict(self) -> dict:
        slots = {}
        for slot, v in self.current_stage.game_logic.players_slots.items():
            if v in self.server.alive_connections:
                nickname = self.server.alive_connections[v].nickname
            elif v == self.setup_stage.game_logic.BOT_TOKEN:
                nickname = 'Bot'
            else:
                nickname = ''

            slots[slot] = (v, nickname)

        return {CommonReqConst.PlayersSlots: slots}

    @property
    def setup_logic(self) -> SettingsStage:
        return self.setup_stage.game_logic
