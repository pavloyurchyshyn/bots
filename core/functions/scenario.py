from typing import Tuple, Optional
from global_obj.main import Global
from core.player.player import PlayerObj
from core.mech.skills.skill import BaseSkill
from core.mech.mech import BaseMech
from core.player.scenario import Scenario
from core.validators.errors import PlayerDoesntOwnSkillValError, SkillNotInPullValError
from core.player.scenario import NoEmptyStepError
from core.player.action import SkipAction, Action

def recalculate_scenario(player: PlayerObj):
    scenario: Scenario = player.scenario
    mech_copy: BaseMech = player.mech

    for action_num, action in tuple(scenario.actions.items()):
        if action is None:
            continue

        mech_copy = mech_copy.get_copy()
        action.mech_copy = mech_copy

        if action.skip:
            action.make_valid()
        else:
            tile_xy: Tuple[int, int]  = action.target_xy
            skill: BaseSkill = action.skill
            if skill:
                try:
                    skill.validate_use(player=player,
                                       target_xy_coord=tile_xy,
                                       mech=mech_copy,
                                       **Global.get_dict_for_validations(),
                                       )

                except (PlayerDoesntOwnSkillValError, SkillNotInPullValError):
                    scenario.cancel_action(action_num)
                    Global.logger.error(f'Skill {skill} disappeared from pool.')
                    continue

                except Exception as e:
                    Global.logger.warning(f'Error during scenario recalculation for {skill} {action.slot}: {e}')
                    action.make_invalid()

                else:
                    action.make_valid()

                skill.use(player=player, target_xy=tile_xy, mech=mech_copy, game_obj=Global.game, skill_cast_uid=action.skill_cast_uid)
                action.mech_copy = mech_copy

            else:
                scenario.cancel_action(action_num)


def get_free_slot_id(player: PlayerObj) -> Optional[int]:
    for slot, action in player.scenario.actions.items():
        if action is None:
            return slot

def skip_action(slot: int, player: PlayerObj):
    if player.scenario.is_full:
        raise NoEmptyStepError

    action_id = slot
    mech = player.mech.get_copy()

    if action_id != 0:
        prev_action_id = action_id - 1
        while prev_action_id >= 0:
            prev_action: Action = player.scenario.actions.get(prev_action_id)
            if prev_action is None:
                pass

            elif prev_action is None and prev_action_id == 0:
                mech = player.mech.get_copy()
                break

            else:
                mech = prev_action.mech_copy.get_copy()
                break

            prev_action_id -= 1

    player.scenario.skip_action(slot=action_id, mech_copy=mech)
