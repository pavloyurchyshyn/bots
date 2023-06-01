from core.player.player import PlayerObj
from server_stuff.player_client import Client
from server_stuff.constants.requests import GameStgConst as GSC
from server_stuff.server_game_proxy.game_stage.components.abs import ComponentAbs
from global_obj.main import Global
from core.mech.skills.constants import Targets
from core.player.scenario import NoEmptyStep


class SkillUseLogic(ComponentAbs):

    def __init__(self):
        self.actions[GSC.SkillM.UseSkill] = self.process_skill_use


    def process_skill_use(self, action: str, client: Client, action_data, player_obj: PlayerObj, *_, **__):
        skill_uid = action_data[GSC.SkillM.SkillUID]
        skill = player_obj.get_latest_scenario_skill(skill_uid)
        tile_xy = tuple(map(int, action_data[GSC.SkillM.UseAttrs][Targets.Tile]))  # TODO for not target skills
        if skill:
            try:
                skill.validate_use(player=player_obj,
                                   target_xy_coord=tile_xy,
                                   mech=player_obj.latest_scenario_mech,
                                   **Global.get_dict_for_validations(), )
                mech_copy = player_obj.latest_scenario_mech
                skill.use(player=player_obj, target_xy=tile_xy, mech=mech_copy, game_obj=Global.game)
                player_obj.scenario.create_and_add_action(use_attrs=action_data[GSC.SkillM.UseAttrs],
                                                      mech_copy=mech_copy, skill_uid=skill_uid)
            except NoEmptyStep as e:
                pass # TODO send data update

            except Exception as e:
                Global.logger.warning(f'{str(Client)} failed to use card: {action_data}')
                Global.logger.warning(f'Reason: {e}')

            else:
                client.sync_send_json({action: action_data})
        else:
            Global.logger.warning(f'User {client} tried to use skill which not exists.')
            # TODO send data update