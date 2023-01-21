import socket
import time
import _thread
from global_obj.main import Global
from game_client.game_match.stages.abs import Processor
from game_client.game_match.stages.setup_proc import SetupStage
from game_client.game_match.stages.match_proc import MatchStage
# from game_client.server_interactions.network.client import SocketConnectionNetwork
from server_stuff.constants.stages import ServerStages
from server_stuff.constants.start_and_connect import LoginArgs
from visual.UI.ok_popup import OkPopUp
from settings.localization.menus.UI import UILocal


class Game:
    def __init__(self, game_body):
        self.setup_processor: SetupStage = None
        self.match_processor: MatchStage = None
        self.game_body = game_body

        # self.current_processor: Processor = None
        self.current_processor: SetupStage = None

        self.alive: bool = True
        self.kill_thread: bool = False

    def update(self):
        self.current_processor.update()

    def connect(self):
        Global.logger.info(f'Connecting to {Global.network_data.anon_host}')
        Global.connection.connect(Global.network_data.server_addr)
        Global.logger.info('Socket connection created')
        Global.logger.info(f'Sending creds: {Global.network_data.credentials}')
        Global.connection.send_json(Global.network_data.credentials)
        response = Global.connection.recv_json()
        Global.logger.debug(f'Response: {response}')
        if response[LoginArgs.Connected]:
            self.process_connection(response)
        else:
            Global.stages.close_game()
            return

    def process_connection(self, response: dict):
        if not response.get(LoginArgs.Connected):
            raise NotImplementedError('Add some info why failed')

        elif response[ServerStages.SERVER_STAGE] == ServerStages.GameSetup:
            Global.logger.info(f'Connection to {ServerStages.GameSetup} stage')
            self.connect_to_setup(response)
            self.wait_for_ready_and_start_thread()

        elif response[ServerStages.SERVER_STAGE] == ServerStages.Game:
            Global.logger.info(f'Connection to {ServerStages.Game} stage')
            self.connect_to_game(response)
            self.wait_for_ready_and_start_thread()

        else:
            raise NotImplementedError('Unknown stage')

    def wait_for_ready_and_start_thread(self):
        # while not Global.connection.recv_json().get('ready'):
        #     time.sleep(0.1)
        Global.logger.info('Player thread on server is ready')
        self.start_recv_thread()

    def connect_to_setup(self, response):
        self.current_processor = self.setup_processor = SetupStage(self, response.get(LoginArgs.IsAdmin, False))
        self.current_processor.connect(response)

    def connect_to_game(self, response):
        Global.logger.debug(f'Loading game: {response}')
        self.match_processor = MatchStage(self, response.get(LoginArgs.IsAdmin, False))
        self.match_processor.connect(response)
        self.current_processor = self.match_processor

    def start_recv_thread(self):
        _thread.start_new_thread(self.recv_thread, ())

    def recv_thread(self):
        Global.logger.info('Started recv thread')
        num = Global.connection.conn_num
        while self.alive and Global.connection:
            try:
                r = Global.connection.recv_json()
            except Exception as e:
                Global.logger.info(f'Got thread error: {e}')
                Global.logger.info(f'Kill thread: {self.kill_thread}')
                Global.logger.info(f'Current conn num: {Global.connection.conn_num} and old {num}')
                if self.kill_thread or not Global.connection or Global.connection.conn_num != num:
                    return
                self.process_thread_exception(e)
            else:
                self.current_processor.process_req(r)

        Global.logger.info(f'Recv server stopped')

    def process_thread_exception(self, e: Exception):
        Global.logger.error(f'Thread exception: {e}')
        try:
            raise e
        except (ConnectionError, ConnectionResetError):
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
        self.kill_thread = True

    def __del__(self):
        self.close()
