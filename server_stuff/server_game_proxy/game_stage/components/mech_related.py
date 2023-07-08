from typing import Tuple
from core.player.player import PlayerObj
from server_stuff.player_client import Client
from server_stuff.constants.requests import GameStgConst as GSC, CommonReqConst as ComReq
from server_stuff.server_game_proxy.game_stage.components.abs import ComponentAbs
from global_obj.main import Global
from core.mech.skills.constants import Targets
from core.player.scenario import NoEmptyStepError
from core.validators.errors import PlayerDoesntOwnSkillValError, SkillNotInPullValError
from core.functions.scenario import recalculate_scenario, skip_action


class MechRelatedLogic(ComponentAbs):

    def __init__(self):
        self.actions[GSC.Mech.Effects] = self.get_mech_effects

    def get_mech_effects(self, action: str, client: Client, player_obj: PlayerObj, **__):
        mech = player_obj.latest_scenario_mech
        if mech:
            effects = [effect.get_dict() for effect in mech.effects]
        else:
            effects = ()

        client.sync_send_json({action: effects})
        print(Global.mech_serializer.mech_to_dict(mech))
