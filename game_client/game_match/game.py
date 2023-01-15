import socket
import time
import _thread
from global_obj.main import Global
from game_client.game_match.stages.abs import Processor
from game_client.game_match.stages.setup import SetupStage
from game_client.server_interactions.server_runner import ServerRunner
# from game_client.server_interactions.network.client import SocketConnectionNetwork
from server_stuff.constants.stages import ServerStages
from server_stuff.constants.start_and_connect import LoginArgs
from visual.UI.ok_popup import OkPopUp
from settings.localization.menus.UI import UILocal


class Game:
    def __init__(self, game_body):
        self.server_runner: ServerRunner = None
        self.setup_processor: SetupStage = None
        self.game_body = game_body

        # self.current_processor: Processor = None
        self.current_processor: SetupStage = None

        self.connect()
        self.alive = True

    def update(self):
        self.current_processor.update()

    def connect(self):
        Global.logger.info(f'Connecting to {Global.network_data.anon_host}')
        Global.connection.connect(Global.network_data.server_addr)
        Global.logger.info('Socket connection created')
        Global.logger.info(f'Sending creds: {Global.network_data.credentials}')
        Global.connection.send_json(Global.network_data.credentials)
        response = Global.connection.recv_json()
        if response[LoginArgs.Connected]:
            Global.logger.info(f'Response: {response}')
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
        while not Global.connection.recv_json().get('ready'):
            time.sleep(0.1)
        Global.logger.info('Player thread on server is ready')
        self.start_recv_thread()

    def connect_to_setup(self, response):
        self.current_processor = self.setup_processor = SetupStage(self, response)

    def connect_to_game(self, response):
        pass

    def start_recv_thread(self):
        _thread.start_new_thread(self.recv_thread, ())

    def recv_thread(self):
        Global.logger.info('Started recv thread')
        while self.alive and Global.connection:
            try:
                r = Global.connection.recv_json()
                self.current_processor.process_req(r)
            except ConnectionError as e:
                if self.alive and Global.connection.alive:
                    self.process_error(e)
                    self.add_popup_to_mmenu(UILocal.Errors.ConnectionLost)
            except AttributeError as e:
                Global.stages.close_game()
                self.alive = False
            except OSError as e:
                Global.logger.warning(str(e))
                if not Global.connection.alive:
                    self.process_error(e)
            except Exception as e:
                self.process_error(e)
                self.add_popup_to_mmenu(UILocal.Errors.UnknownError)
        Global.logger.info(f'Recv server stopped')

    def process_error(self, e: Exception):
        # TODO make normal text
        # if self.alive and Global.connection.alive:
        Global.logger.error(str(e))
        Global.stages.close_game()
        self.alive = False

    def add_popup_to_mmenu(self, msg: str, raw: bool = False):
        self.game_body.main_menu.add_popup(OkPopUp('error_popup',
                                                   text=msg,
                                                   raw_text=raw,
                                                   parent=self.game_body.main_menu))

    def close(self):
        self.alive = False
        Global.connection.close()

    def __del__(self):
        self.close()
