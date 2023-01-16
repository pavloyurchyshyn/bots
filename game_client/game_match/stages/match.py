from game_client.game_match.stages.abs import Processor


# TODO
class MathStage(Processor):

    def __init__(self, game, admin: bool):
        super(MathStage, self).__init__(admin=admin)
        self.game = game

    def process_req(self, r: dict):
        pass

    def update(self):
        pass

    def connect(self, response: dict):
        pass
