from core.player.player import PlayerObj


class BotPlayer:
    """ Bot which should decide what to do"""

    def __init__(self, slot: int, player_obj: PlayerObj):
        self.slot = slot
        self.player_obj: PlayerObj = player_obj

    def decide(self):
        pass
