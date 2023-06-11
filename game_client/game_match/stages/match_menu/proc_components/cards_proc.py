from global_obj.main import Global
from server_stuff.constants.requests import GameStgConst as GSC
from visual.cards.skill.skill_cards_fabric import SkillsCardsFabric
from core.mech.skills.constants import Targets
from core.mech.mech import BaseMech
from core.player.player import PlayerObj
from settings.localization.validation import ValidationMsg
from core.functions.scenario import recalculate_scenario, skip_action


class CardsProc:
    actions: dict
    player: PlayerObj

    def __init__(self):
        self.actions[GSC.SkillM.SelectSkill] = self.process_select_card
        self.actions[GSC.SkillM.UseSkill] = self.process_use_card
        self.actions[GSC.SkillM.ScenarioIsFull] = self.scenario_is_full
        self.actions[GSC.SkillM.CancelSkillUse] = self.cancel_skill_use
        self.actions[GSC.SkillM.SkipCommand] = self.process_skip

    def cancel_skill_use(self, *_, request_data, **__):
        for slot in request_data:
            slot = int(slot)
            self.player.scenario.cancel_action(slot)
            Global.logger.info(f'Canceled action {slot}')

        recalculate_scenario(self.player)
        self.UI.collect_skills_deck()

    def process_skip(self, *_, request_data, **__):
        skip_action(int(request_data), player=self.player)
        recalculate_scenario(self.player)

    def scenario_is_full(self, *_, **__):
        self.UI.add_ok_popup(ValidationMsg.NoEmptyStepError)

    def process_use_card(self, *_, request_data, **__):
        Global.logger.info(f'Use skill {request_data}')
        skill_uid = request_data[GSC.SkillM.SkillUID]
        is_valid = request_data[GSC.SkillM.SkillValid]
        tile_xy = tuple(map(int, request_data[GSC.SkillM.UseAttrs][Targets.Tile]))
        mech_copy: BaseMech = self.player.latest_scenario_mech.get_copy()
        action_id = request_data.get(GSC.SkillM.ActionID, None)

        skill = tuple(filter(lambda s: s.unique_id == skill_uid, mech_copy.skills))[0]
        skill.use(player=self.player, target_xy=tile_xy, mech=mech_copy, game_obj=Global.game)
        self.player.scenario.create_and_add_action(use_attrs=request_data[GSC.SkillM.UseAttrs],
                                                   mech_copy=mech_copy, skill_uid=skill_uid,
                                                   valid=is_valid, slot=action_id)

        recalculate_scenario(player=self.player)
        self.UI.collect_skills_deck()


    def process_select_card(self, r: dict):
        skill_uid = r[GSC.SkillM.SelectSkill]
        if skill_uid == GSC.SkillM.UnknownSkill:  # TODO maybe just sync data
            self.UI.add_ok_popup(f'Unknown skill {skill_uid}')
            return

        for card in self.UI.skills_deck:
            if card.skill.unique_id == skill_uid:
                self.UI.selected_card_to_use = card
                break
            else:
                Global.logger.info(f'Card {skill_uid} not in deck.')

    @property
    def skill_cards_fabric(self) -> SkillsCardsFabric:
        return self.UI.skill_cards_fabric