from global_obj import Global
from constants.stages import StagesConstants
from game_client.stages import *


class Game:
    """
    Main class
    """

    def __init__(self, launch_obj):
        self.launch_obj = launch_obj

        self.stages_dict = {
            StagesConstants.MainMenu: self.update_main_menu,
            StagesConstants.SoloGameMenu: self.update_new_game_menu,
            StagesConstants.MapEditor: self.update_map_editor,
            StagesConstants.CloseGame: self.close_game,

        }

        self.main_menu = MainMenu()
        self.new_game_menu = NewGame()
        self.map_editor = MapEditor()

    def game_loop(self):
        self.stages_dict[Global.stages.current_stage]()

        self.check_alt_and_f4()

    def update_main_menu(self):
        self.main_menu.update()

    def update_new_game_menu(self):
        self.new_game_menu.update()

    def update_map_editor(self):
        self.map_editor.update()

    def close_game(self):
        self.launch_obj.close_game()

    def check_alt_and_f4(self):
        # TODO if in round_stage -> save game
        if Global.keyboard.alt_and_f4:
            pass
