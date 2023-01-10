from game_client.stages.setup_menu.UI import SetupMenu
from game_client.game_match.stages.abs import Processor
from server_stuff.constants.start_and_connect import LoginArgs


class SetupStage(Processor):
    def __init__(self, game_stage, r: dict):
        super(SetupStage, self).__init__(r[LoginArgs.IsAdmin])
        self.exception = None
        self.game_stage = game_stage
        self.UI = SetupMenu()

    def process_req(self, r: dict):
        print(r)

    def update(self):
        self.UI.update()
        if self.exception:
            raise self.exception
