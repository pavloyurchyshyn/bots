from global_obj.main import Global

from visual.UI.base.menu import Menu
from visual.UI.popup_controller import PopUpsController
from visual.UI.base.mixins import DrawElementBorderMixin

from core.mech.base.mech import BaseMech

from game_client.game_match.stages.match_menu.components.chat import ChatC
from game_client.game_match.stages.match_menu.components.mech import MechC
from game_client.game_match.stages.match_menu.components.tasks import TasksC
from game_client.game_match.stages.match_menu.components.world import WorldC
from game_client.game_match.stages.match_menu.components.ready import ReadyW
from game_client.game_match.stages.match_menu.components.tile import TileInfoC
from game_client.game_match.stages.match_menu.components.cards_deck import CardsC
from game_client.game_match.stages.match_menu.components.used_cards import UsedCardsC
from game_client.game_match.stages.match_menu.components.hp_and_mana import HpAndManaC

from game_client.game_match.stages.match_menu.settings.buttons import BUTTONS_DATA


class GameMatch(Menu, PopUpsController,
                WorldC, ChatC, MechC,
                CardsC, UsedCardsC,
                TileInfoC, TasksC, HpAndManaC,
                DrawElementBorderMixin,
                ):

    def __init__(self, processor):
        self.player = processor.player
        self.ready_win = ReadyW(self)
        self.processor = processor
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
    def mech(self) -> BaseMech:
        return self.player.mech
