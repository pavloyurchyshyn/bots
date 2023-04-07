import os
from logging import Logger
from global_obj.clock import Clock
from global_obj.stages import Stages
from global_obj.logger import get_logger

from core.mech.base.pools.skills_pool import SkillsPool
from core.mech.base.pools.details_pool import DetailsPool
from core.mech.base.mech_serializer import MechSerializer

# from game_logic.game_data.id_generator import IdGenerator

__all__ = 'Global',

VisualPygameOn = os.environ.get('VisualPygameOn', 'on') == 'on'


class Global:
    """
    Object for global in-game parameters.
    """
    logger: Logger = get_logger()
    clock: Clock = Clock()  # global for all game
    stages: Stages = Stages(logger)
    round_clock: Clock = Clock()  # not counting on pause etc.
    test_draw = False

    game = None
    details_pool: DetailsPool = None
    skill_pool: SkillsPool = None
    mech_serializer: MechSerializer = None  # MechSerializer(details_pool)

    # id_generator = IdGenerator()
    # players_data: PlayersData = PlayersData()

    if VisualPygameOn:
        from pygame import Surface as __Surface
        from global_obj.mouse import Mouse as __mouse
        from global_obj.keyboard import Keyboard as __keyboard
        from global_obj.display import MAIN_DISPLAY as __display
        from settings.network import NetworkData as __NetworkData
        from settings.localization import LocalizationLoader as __localization
        from visual.textures.textures import Textures as __Textures
        from game_client.server_interactions.websocket_connection import WebSocketConnection as __WebSocketConnection

        display: __Surface = __display
        keyboard = __keyboard(logger)
        mouse = __mouse()
        localization = __localization()
        loc = localization
        network_data = __NetworkData()
        textures: __Textures = __Textures()
        connection: __WebSocketConnection = __WebSocketConnection()
        # TODO add sound

    @classmethod
    def set_game_obj(cls, game):
        cls.game = game
        cls.details_pool: DetailsPool = game.details_pool
        cls.skill_pool: SkillsPool = game.skills_pool
        cls.mech_serializer: MechSerializer = MechSerializer(game.details_pool)

    @classmethod
    def del_game_obj(cls):
        cls.game = None


if __name__ == '__main__':
    pass
