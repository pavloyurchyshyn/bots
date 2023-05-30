import os
from logging import Logger
from global_obj.clock import Clock
from global_obj.stages import Stages
from global_obj.logger import get_logger

from core.validators.constants import ValidationKeys

from interfaces.skills_pool_interface import SkillsPoolInterface
from interfaces.details_pool_interface import DetailsPoolInterface
from interfaces.mech_serializer_interface import MechSerializerInterface

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
    details_pool: DetailsPoolInterface = None
    skill_pool: SkillsPoolInterface = None
    mech_serializer: MechSerializerInterface = None  # MechSerializer(details_pool)

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
        cls.details_pool: DetailsPoolInterface = game.details_pool
        cls.skill_pool: SkillsPoolInterface = game.skills_pool
        from core.mech.mech_serializer import MechSerializer
        cls.mech_serializer: MechSerializer = MechSerializer(game.details_pool)

    @classmethod
    def del_game_obj(cls):
        cls.game = None
        cls.details_pool: DetailsPoolInterface = None
        cls.skill_pool: SkillsPoolInterface = None
        cls.mech_serializer = None

    @classmethod
    def get_dict_for_validations(cls):
        return {
            ValidationKeys.Global: cls,
            ValidationKeys.GameObj: cls.game,
            ValidationKeys.SkillPool: cls.skill_pool,
            ValidationKeys.DetailsPool: cls.details_pool,
            ValidationKeys.AllMeches: tuple([player.mech for player in cls.game.players.values()]) if cls.game else None,
            ValidationKeys.Players: cls.game.players if cls.game else None,
            ValidationKeys.World: cls.game.world if cls.game else None,
        }

if __name__ == '__main__':
    pass
