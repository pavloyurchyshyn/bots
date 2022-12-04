from global_obj import Global
from constants.stages import StagesConstants
from game_client.stages import MainMenu, NewGame


class Game:
    """
    Main class
    """

    def __init__(self, launch_obj):
        self.launch_obj = launch_obj

        self.stages_dict = {
            StagesConstants.MainMenu: self.update_main_menu,
            StagesConstants.CloseGame: self.close_game,
            StagesConstants.SoloGameMenu: self.update_new_game_menu,

        }

        self.main_menu = MainMenu()
        self.new_game_menu = NewGame()

    def game_loop(self):
        self.stages_dict[Global.stages.current_stage]()

        self.check_alt_and_f4()

    def update_main_menu(self):
        self.main_menu.update()

    def update_new_game_menu(self):
        self.new_game_menu.update()

    def close_game(self):
        pass
        self.launch_obj.close_game()

    def check_alt_and_f4(self):
        # TODO if in round_stage -> save game
        if Global.keyboard.alt_and_f4:
            pass
