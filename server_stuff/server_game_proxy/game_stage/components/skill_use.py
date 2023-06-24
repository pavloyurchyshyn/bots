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


class SkillUseLogic(ComponentAbs):

    def __init__(self):
        self.actions[GSC.SkillM.UseSkill] = self.process_skill_use
        self.actions[GSC.SkillM.CancelSkillUse] = self.process_cancel_action
        self.actions[GSC.SkillM.SkipCommand] = self.process_skip_action

    def process_cancel_action(self, action: str, client: Client,
                              action_data: Tuple[int], player_obj: PlayerObj,
                              *_, **__):
        for action_id in action_data:
            player_obj.scenario.cancel_action(action_id)
            Global.logger.info(f'{str(client)} canceled action {action_data}')

        recalculate_scenario(player=player_obj)

        client.sync_send_json({action: action_data})

    def process_skip_action(self, action: str, client: Client,
                            action_data: int, player_obj: PlayerObj,
                            *_, **__):
        try:
            action_id = int(action_data)
        except ValueError:
            client.sync_send_json({ComReq.InfoPopUp: 'Bad action slot'})
            return

        if action_id < 0:
            client.sync_send_json({ComReq.InfoPopUp: 'Bad action slot'})
            return

        try:
            skip_action(slot=action_id, player=player_obj)
        except NoEmptyStepError:
            # TODO sync data
            Global.logger.warning(f'Player {client} has no empty slots')
            client.sync_send_json({GSC.SkillM.ScenarioIsFull: True})
        else:
            client.sync_send_json({action: action_data})


    def process_skill_use(self, action: str, client: Client, action_data: dict, player_obj: PlayerObj, *_, **__):
        skill_uid = action_data[GSC.SkillM.SkillUID]
        mech_copy = player_obj.latest_scenario_mech.get_copy()
        skill = player_obj.get_latest_scenario_skill(skill_uid, mech=mech_copy)
        tile_xy = tuple(map(int, action_data[GSC.SkillM.UseAttrs][Targets.Tile]))  # TODO for not target skills
        invalid_use = action_data.get(GSC.SkillM.InvalidUse, False)
        action_id = int(action_data.get(GSC.SkillM.ActionID, None))
        if skill:
            skill_cast_uid: str = f'{client.slot}_{Global.rounds_clock.current_round}_{Global.game.id_generator}'
            try:
                skill.validate_use(player=player_obj,
                                   target_xy_coord=tile_xy,
                                   mech=player_obj.latest_scenario_mech,
                                   **Global.get_dict_for_validations(),
                                   )

            except NoEmptyStepError as e:
                client.sync_send_json({GSC.SkillM.ScenarioIsFull: True})
                Global.logger.warning(f'Player {client} has no empty slots')

            except(PlayerDoesntOwnSkillValError, SkillNotInPullValError) as e:
                Global.logger.warning(f'{client}: {e}')
                # TODO send update

            except Exception as e:
                action_data[GSC.SkillM.SkillValid] = False
                action_data[GSC.SkillM.SkillCastUID] = skill_cast_uid
                if invalid_use:
                    skill.use(player=player_obj, target_xy=tile_xy, mech=mech_copy, game_obj=Global.game,
                              skill_cast_uid=skill_cast_uid)
                    player_obj.scenario.create_and_add_action(use_attrs=action_data[GSC.SkillM.UseAttrs],
                                                              mech_copy=mech_copy, skill_uid=skill_uid, slot=action_id)
                    client.sync_send_json({action: action_data})
                else:
                    Global.logger.warning(f'{client} failed to use card: {action_data}')
                    Global.logger.warning(f'Reason: {e}')

            else:
                skill.use(player=player_obj, target_xy=tile_xy,
                          mech=mech_copy, game_obj=Global.game, skill_cast_uid=skill_cast_uid)
                action_data[GSC.SkillM.SkillValid] = True
                player_obj.scenario.create_and_add_action(use_attrs=action_data[GSC.SkillM.UseAttrs],
                                                          mech_copy=mech_copy, skill_uid=skill_uid, slot=action_id)
                recalculate_scenario(player_obj)
                Global.logger.info(f'{client} used card: {action_data}')
                client.sync_send_json({action: action_data})
        else:
            Global.logger.warning(f'User {client} tried to use skill which not exists.')
            # TODO send data update