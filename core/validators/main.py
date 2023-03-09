from global_obj.main import Global
from core.player.player import Player
from core.world.base.logic.world import LogicWorld
from core.mech.base.pools.details_pool import DetailsPool


class ValidatorsCollection:
    @staticmethod
    def example_validation(world: LogicWorld, player: Player, details_pool, players, skill_uid, **kwargs):
        return True