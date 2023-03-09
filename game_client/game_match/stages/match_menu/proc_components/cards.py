from global_obj.main import Global
from server_stuff.constants.game_stage import GameStgConst as GSC
from visual.cards.skill.skill_cards_fabric import SkillsCardsFabric


class CardsProc:
    actions: dict

    def __init__(self):
        self.actions[GSC.SkillM.SelectSkill] = self.process_select_card
        self.actions[GSC.SkillM.UseSkill] = self.process_use_card
        self.actions[GSC.SkillM.ScenarioIsFull] = self.ScenarioIsFull

    def ScenarioIsFull(self, r: dict):
        self.UI.add_ok_popup(f'Scenario is full.')

    def process_use_card(self, r: dict):
        print(r)
        # TODO use card

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