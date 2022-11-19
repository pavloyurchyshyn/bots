from global_obj import Global
from core.game_global import GameGlobal
from constants.stages import StagesConstants
from game.stages import MainMenu


def close_game():
    from pygame import quit as close_program_pygame
    import sys

    close_program_pygame()
    sys.exit()


class Game:
    """
    Main class
    """

    def __init__(self, launch_obj):
        self.launch_obj = launch_obj

        self.stages_dict = {
            StagesConstants.MainMenu: self.update_main_menu,
            StagesConstants.CloseGame: close_game,

        }

        self.main_menu = MainMenu()

    def game_loop(self):
        self.stages_dict[GameGlobal.stages.current_stage]()

        self.check_alt_and_f4()

    def update_main_menu(self):
        self.main_menu.update()

    def check_alt_and_f4(self):
        # TODO if in round_stage -> save game
        if Global.keyboard.alt_and_f4:
            close_game()
