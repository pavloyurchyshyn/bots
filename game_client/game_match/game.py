import time
import _thread
from global_obj import Global
from game_client.game_match.stages.abs import Processor
from game_client.game_match.stages.setup import SetupStage
from game_client.server_interactions.server_runner import ServerRunner
from game_client.server_interactions.network.client import SocketConnectionNetwork
from server_stuff.constants.stages import ServerStages
from server_stuff.constants.start_and_connect import LoginArgs
from visual.UI.ok_popup import OkPopUp
from settings.localization.menus.UI import UILocal


class Game:
    def __init__(self, game_body, run_server):
        self.client: SocketConnectionNetwork = SocketConnectionNetwork()
        self.server_runner: ServerRunner = None

        self.setup_processor: SetupStage = None
        self.game_body = game_body

        if run_server:
            self.server_runner = ServerRunner(token=self.client.token)
            self.server_runner.run()

        self.current_processor: Processor = None

        self.connect()
        self.alive = True

    def update(self):
        self.current_processor.update()

    def connect(self):
        r = self.client.connect()
        self.process_connection(r)

        while not self.client.connection.recv_json().get('ready'):
            time.sleep(0.1)
        Global.logger.info('Player thread on server is ready')
        self.start_recv_thread()

    def process_connection(self, response: dict):
        if not response.get(LoginArgs.Connected):
            raise NotImplementedError('Add some info why failed')

        elif response[ServerStages.SERVER_STAGE] == ServerStages.GameSetup:
            Global.logger.info(f'Connection to {ServerStages.GameSetup}')
            self.connect_to_setup(response)

        elif response[ServerStages.SERVER_STAGE] == ServerStages.Game:
            Global.logger.info(f'Connection to {ServerStages.Game}')
            self.connect_to_game(response)

        else:
            raise NotImplementedError('Unknown stage')

    def connect_to_setup(self, response):
        self.current_processor = self.setup_processor = SetupStage(self, response)

    def connect_to_game(self, response):
        pass

    def start_recv_thread(self):
        _thread.start_new_thread(self.recv_thread, ())

    def recv_thread(self):
        Global.logger.info('Started recv thread')
        while self.alive:
            try:
                r = self.client.connection.recv_json()
                self.current_processor.process_req(r)
            except ConnectionError as e:
                self.process_error(e, UILocal.Errors.ConnectionLost)
            except Exception as e:
                self.process_error(e, UILocal.Errors.UnknownError)

    def process_error(self, e, msg: str, raw: bool = False):
        self.alive = False
        Global.logger.error(str(e))
        # TODO make normal text
        self.game_body.main_menu.add_popup(OkPopUp('error_popup',
                                                   text=msg,
                                                   raw_text=raw,
                                                   parent=self.game_body.main_menu))
        Global.stages.close_game()

    def close(self):
        self.alive = False
        if self.server_runner:
            self.server_runner.stop()
            self.server_runner = None
        if self.client:
            self.client.disconnect()
            self.client = None

    def __del__(self):
        self.close()
