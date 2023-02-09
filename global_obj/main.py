import os
from logging import Logger
from global_obj.clock import Clock
from global_obj.stages import Stages
from global_obj.logger import get_logger
from core.mech.base.pools.skills_pool import SkillsPool
from core.mech.base.pools.details_pool import DetailsPool
from core.game_logic.game_components.game_data.id_generator import IdGenerator

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

    if VisualPygameOn:
        from pygame import Surface as __Surface
        from global_obj.mouse import Mouse as __mouse
        from global_obj.keyboard import Keyboard as __keyboard
        from global_obj.display import MAIN_DISPLAY as __display
        from settings.network import NetworkData as __NetworkData
        from settings.localization import LocalizationLoader as __localization
        from game_client.server_interactions.network.socket_connection import SocketConnection as __SC
        from visual.textures.textures import Textures as __Textures

        display: __Surface = __display
        keyboard = __keyboard(logger)
        mouse = __mouse()
        localization = __localization()
        loc = localization
        network_data = __NetworkData()
        connection = __SC(logger=logger)
        textures: __Textures = __Textures()
        # TODO add sound

    id_generator = IdGenerator()
    details_pool: DetailsPool = DetailsPool(id_generator)
    skill_pool: SkillsPool = details_pool.skills_pool


if __name__ == '__main__':
    Global.logger.info(f'Connecting to {Global.network_data.anon_host}')
    Global.connection.connect(Global.network_data.server_addr)
    Global.logger.info('Socket connection created')
    Global.logger.info(f'Sending creds: {Global.network_data.credentials}')
    Global.connection.send_json(Global.network_data.credentials)
    response = Global.connection.recv_json()
    print(response)
