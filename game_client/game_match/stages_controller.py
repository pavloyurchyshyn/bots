import json
import _thread
from typing import Dict
from global_obj.main import Global
from core.player.player import PlayerObj
from visual.UI.ok_popup import OkPopUp
from settings.localization.menus.UI import UILocal
from game_logic.constants.stages import ServerStages
from server_stuff.constants.start_and_connect import LoginArgs
from game_client.game_match.stages.setup_proc import SetupStage
from game_client.game_match.stages.match_proc import MatchStage


class StagesController:
    def __init__(self, game_body):
        self.setup_processor: SetupStage = None
        self.match_processor: MatchStage = None
        self.game_body = game_body

        # self.current_processor: Processor = None
        self.current_processor: SetupStage = None

        self.alive: bool = True
        # self.kill_thread: bool = False
        # self.client = None
        # self.player: PlayerObj = None
        # self.other_players: Dict[str, PlayerObj] = {}

    def update(self):
        self.current_processor.update()

    def connect(self):
        Global.logger.info(f'Connecting to {Global.network_data.anon_host}')
        Global.connection.connect(f'ws://{Global.network_data.address}:{Global.network_data.port}')
        Global.logger.info('Socket connection created')
        Global.logger.info(f'Sending creds: {Global.network_data.credentials}')
        Global.connection.send_json(Global.network_data.credentials)
        response = Global.connection.recv_json()
        Global.logger.warning(f'Response: {response}')
        Global.logger.warning(f"Player client data: {response.get(LoginArgs.ClientAttrs.ClientData)}")

        client_data = response.get(LoginArgs.ClientAttrs.ClientData, {})
        Global.network_data.token = client_data[LoginArgs.Token]
        Global.network_data._is_admin = client_data[LoginArgs.ClientAttrs.IsAdmin]
        if response[LoginArgs.Result.Status] == LoginArgs.Result.Connected:
            self.process_connection(response)
        else:
            Global.stages.close_game()
            return

    def process_connection(self, response: dict):
        Global.logger.info(f'Connection data: {response}')
        if not response.get(LoginArgs.Result.Status):
            raise NotImplementedError('Add some info why failed')

        elif response[ServerStages.SERVER_STAGE] == ServerStages.GameSetup:
            Global.logger.info(f'Connection to {ServerStages.GameSetup} stage')
            self.connect_to_setup(response)
            self.send_ready_and_start_thread()

        elif response[ServerStages.SERVER_STAGE] == ServerStages.Game:
            Global.logger.info(f'Connection to {ServerStages.Game} stage')
            self.connect_to_game(response)
            self.send_ready_and_start_thread()

        else:
            raise NotImplementedError('Unknown stage')

    def send_ready_and_start_thread(self):
        # while not Global.connection.recv_json().get('ready'):
        #     time.sleep(0.1)
        Global.connection.send_json({'ready': True})
        Global.logger.info('Player thread on server is ready')
        self.start_recv_thread()

    def connect_to_setup(self, response):
        self.current_processor = self.setup_processor = SetupStage(self, Global.network_data.is_admin)
        self.current_processor.connect(response)

    def connect_to_game(self, response):
        Global.logger.info(f'Loading game: {response}')
        self.match_processor = MatchStage(self, Global.network_data.is_admin)
        self.match_processor.connect(response)
        self.current_processor = self.match_processor

    def start_recv_thread(self):
        _thread.start_new_thread(self.recv_thread, ())

    def recv_thread(self):
        Global.logger.info('Started recv thread')
        while self.alive and Global.connection:
            try:
                r = Global.connection.recv_json()
            except ConnectionError as e:
                Global.logger.info(f'Got thread error: {e}')
                if self.alive:
                    self.process_thread_exception(e)
                break
            except Exception as e:
                Global.logger.info(f'Got thread error: {e}')
                self.process_thread_exception(e)
            else:
                self.current_processor.process_req(r)

        Global.logger.info(f'Recv server stopped')

    def process_thread_exception(self, e: Exception):
        Global.logger.error(f'Thread exception: {e}')
        try:
            raise e
        except (ConnectionError, ConnectionResetError, json.JSONDecodeError):
            self.alive = False
            Global.stages.close_game()
            self.add_popup_to_mmenu(UILocal.Errors.ConnectionLost)

    def add_popup_to_mmenu(self, msg: str, raw: bool = False):
        self.game_body.main_menu.add_popup(OkPopUp('error_popup',
                                                   text=msg,
                                                   raw_text=raw,
                                                   parent=self.game_body.main_menu))

    def close(self):
        self.alive = False

    def __del__(self):
        self.close()
