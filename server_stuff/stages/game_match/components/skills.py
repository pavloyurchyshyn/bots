from global_obj.main import Global
from core.player.player import Player
from server_stuff.constants.game_stage import GameStgConst as GSC
from game_client.server_interactions.socket_connection import ConnectionWrapperAbs


class SkillsLogic:
    actions: dict

    def __init__(self):
        self.actions[GSC.SkillM.UseSkill] = self.use_skill
        # self.actions[GSC.SkillM.SelectSkill] = self.get_skill_stats

    # def get_skill_stats(self, connection: ConnectionWrapperAbs, player_obj: Player, request: dict, **kwargs):
    #     skill = Global.skill_pool.get_skill_by_id(request[GSC.SkillM.SelectSkill])
    #
    #     if skill:
    #         if skill in player_obj.skills and (not skill.on_cooldown):
    #             connection.send_json({GSC.SkillM.SelectSkill: skill.unique_id})
    #     else:
    #         connection.send_json({GSC.SkillM.SelectSkill: GSC.SkillM.UnknownSkill})

    def use_skill(self, connection: ConnectionWrapperAbs, player_obj: Player, request: dict, **kwargs):
        use_skill = request[GSC.SkillM.UseSkill]
        skill = Global.skill_pool.get_skill_by_id(use_skill[GSC.SkillM.SkillUID])
        if skill:
            if skill in player_obj.skills and (not skill.on_cooldown):
                if player_obj.scenario.is_full:
                    connection.send_json({GSC.SkillM.ScenarioIsFull: True})
                else:
                    connection.send_json({GSC.SkillM.UseSkill: skill.unique_id})
            else:
                pass
                # TODO maybe sync data
        else:
            connection.send_json({GSC.SkillM.SelectSkill: GSC.SkillM.UnknownSkill})
            # TODO sync stats
