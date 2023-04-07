from global_obj.main import Global

from visual.UI.base.menu import Menu
from visual.cards.skill.card import SkillCard
from visual.UI.popup_controller import PopUpsController
from visual.UI.base.mixins import DrawElementBorderMixin

from core.player.player import PlayerObj
from core.mech.base.mech import BaseMech

from game_client.game_match.stages.match_menu.UI_components.chat import ChatC
from game_client.game_match.stages.match_menu.UI_components.mech import MechC
from game_client.game_match.stages.match_menu.UI_components.tasks import TasksC
from game_client.game_match.stages.match_menu.UI_components.world import WorldC
from game_client.game_match.stages.match_menu.UI_components.ready import ReadyW
from game_client.game_match.stages.match_menu.UI_components.tile import TileInfoC
from game_client.game_match.stages.match_menu.UI_components.card_use import CardUseC
from game_client.game_match.stages.match_menu.UI_components.cards_deck import CardsC
from game_client.game_match.stages.match_menu.UI_components.used_cards import UsedCardsC
from game_client.game_match.stages.match_menu.UI_components.hp_and_mana import HpAndManaC
from game_client.game_match.stages.match_menu.settings.buttons import BUTTONS_DATA

from server_stuff.constants.requests import GameStgConst as GSC
from visual.cards.skill.skill_cards_fabric import SkillsCardsFabric


class GameMatch(Menu, PopUpsController,
                WorldC, ChatC, MechC,
                CardsC, UsedCardsC,
                TileInfoC, TasksC, HpAndManaC,
                DrawElementBorderMixin,
                CardUseC
                ):

    def __init__(self, processor):
        self.processor = processor
        self.ready_win = ReadyW(self)
        self.skill_cards_fabric: SkillsCardsFabric = SkillsCardsFabric(Global.skill_pool)
        super(GameMatch, self).__init__(BUTTONS_DATA)
        PopUpsController.__init__(self)
        WorldC.__init__(self)
        ChatC.__init__(self)
        MechC.__init__(self)
        CardsC.__init__(self)
        UsedCardsC.__init__(self)
        TileInfoC.__init__(self)
        TasksC.__init__(self)
        HpAndManaC.__init__(self)
        CardUseC.__init__(self)

    def update(self):
        Global.display.fill((0, 0, 0))
        collided_popup_btn = self.update_popups()

        self.simple_buttons_update(self.draw_border_around_element)
        self.update_and_draw_map()

        self.draw_popups()
        self.update_chat()

        self.draw_mech_win()

        self.move_cards()
        self.draw_used_cards()
        self.draw_hp_and_mana_win()

        self.draw_cards(dy=self.cards_dy)

        self.ready_win.update()
        self.draw_tile_info()

        self.draw_tasks()
        if collided_popup_btn:
            self.draw_border_around_element(collided_popup_btn)

        if self.selected_card_to_use:
            self.check_for_card_use()
            self.check_for_card_select()
        else:
            self.check_for_card_select()
            self.check_for_card_use()

        self.draw_use_trace()

    def check_for_card_select(self):
        if Global.mouse.l_up:
            if self.get_rect().collidepoint(Global.mouse.pos):
                for card in self.skills_deck:
                    if card.get_rect().collidepoint(Global.mouse.pos):
                        # Global.connection.send_json({GSC.SkillM.SelectSkill: card.skill.unique_id})
                        self.selected_card_to_use: SkillCard = card
                        break
                else:
                    self.unselect_card_to_use()
            else:
                self.unselect_card_to_use()
        elif Global.mouse.r_up:
            self.unselect_card_to_use()

    def unselect_card_to_use(self):
        self.selected_card_to_use = None

    def update_popups(self):
        collided_popup_btn = None
        if self.popups:
            if self.popups[0].collide_point(Global.mouse.pos):
                for btn in self.popups[0].buttons:
                    if btn.collide_point(Global.mouse.pos):
                        collided_popup_btn = btn
                        if Global.mouse.l_up:
                            btn.do_action()
                            if self.popups[0].on_click_action:
                                self.popups[0].on_click_action(self.popups[0], btn)
                            break
                if self.popups and self.popups[0].inactive:
                    self.popups.remove(self.popups[0])
            Global.mouse.l_up = False
            Global.mouse._pos = -10, -10
        return collided_popup_btn

    def move_cards(self):
        if self.cards_deck_collide_point(Global.mouse.pos):
            self.deck_cards_move_check()
        elif self.used_cards_collide_point(Global.mouse.pos):
            self.used_cards_move_check()
        else:
            if self.cards_dy != 0:
                self.cards_dy += self.CARDS_MOVE_SPEED * Global.clock.d_time * (1 if self.cards_dy < 0 else -1)
                if -3 <= self.cards_dy <= 3:
                    self.cards_dy = 0

    @property
    def player(self):
        return self.processor.player

    @property
    def mech(self):
        return self.processor.mech