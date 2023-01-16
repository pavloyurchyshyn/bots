from global_obj.main import Global
from constants.stages import StagesConstants
from game_client.stages import *
from game_client.game_match.game import Game
from game_client.server_interactions.server_runner import ServerRunner


class GameBody:
    """
    Main class
    """

    def __init__(self, launch_obj):
        self.launch_obj = launch_obj

        self.stages_dict = {
            StagesConstants.MainMenu: self.update_main_menu,
            StagesConstants.SoloGameMenu: self.update_new_game_menu,
            StagesConstants.MapEditor: self.update_map_editor,
            StagesConstants.ExitGame: self.exit_game,

            StagesConstants.JoinGameMenu: self.join_game_menu,
            StagesConstants.Host_Stage: self.host,
            StagesConstants.LoadGame: self.join_game,
            StagesConstants.Game: self.update_game,
            StagesConstants.CloseGame: self.close_game,

        }

        self.main_menu = MainMenu()
        self.new_game_menu = NewGame()
        self.map_editor = MapEditor()
        self.join_menu: JoinMenu = JoinMenu()

        self.server_runner: ServerRunner = None
        self.game: Game = None

    def game_loop(self):
        self.stages_dict[Global.stages.current_stage]()

        self.check_alt_and_f4()

    def update_main_menu(self):
        self.main_menu.update()

    def update_new_game_menu(self):
        self.new_game_menu.update()

    def update_map_editor(self):
        self.map_editor.update()

    def exit_game(self):
        self.launch_obj.close_game()

    def join_game_menu(self):
        self.join_menu.update()

    def host(self):
        Global.logger.info('Hosting a game')
        if self.server_runner:
            self.server_runner = None
        self.server_runner = ServerRunner(token=Global.network_data.token)
        self.server_runner.run()
        Global.stages.load_join_game()

    # TODO load and start thread
    def join_game(self):
        """
        Connect to game.
        """
        Global.logger.info('Joining game')
        self.game = Game(self)
        self.game.connect()
        Global.stages.game()

    def update_game(self):
        self.game.update()

    def close_game(self):
        Global.logger.info('Closing game')
        self.game.close()
        self.game: Game = None
        self.server_runner = None
        Global.connection.close()
        Global.stages.main_menu()

    def check_alt_and_f4(self):
        # TODO if in round_stage -> save game
        if Global.keyboard.alt_and_f4:
            pass
