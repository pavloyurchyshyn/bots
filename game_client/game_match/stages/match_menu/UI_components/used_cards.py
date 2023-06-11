from typing import Dict, List, Tuple
from pygame import Surface, Rect
from pygame.draw import rect as draw_rect
from global_obj.main import Global
from server_stuff.constants.requests import GameStgConst as GSC
from settings.visual.cards import SkillCardSize
from core.player.player import PlayerObj
from visual.cards.skill.card import SkillCard
from visual.UI.base.button import Button
from visual.UI.utils import get_surface
from visual.styles import get_red_btn_style
from visual.UI.base.mixins import DrawElementBorderMixin
from game_client.game_match.stages.match_menu.settings.windows_sizes import UsedCards, HpBar


class MoveCancelEl(DrawElementBorderMixin):
    def __init__(self,
                 slot_rect: Rect,
                 x: int, y: int,
                 h_size: int, v_size: int,
                 slot: int,
                 left_active: bool, right_active: bool):
        self.slot_rect = slot_rect

        self.x = x
        self.y = y
        self.h_size = h_size
        self.v_size = v_size
        self.rect = Rect(x, y, h_size, v_size)
        self.real_position = x, y

        self.slot = slot
        self.surface: Surface = None
        self.init_surface()
        self.elements = []

        v_size = 0.90
        elements_count = 1 + left_active + right_active
        h_size_k = 0.9 / elements_count
        space_size = (1 - h_size_k * elements_count) / (1 + elements_count)
        x_k = 0.01 + space_size
        if left_active:
            move_left = Button(uid=f'move_left_{slot}_btn', text='<-',
                               v_size_k=v_size,
                               h_size_k=h_size_k,
                               x_k=x_k,
                               parent=self)
            x_k += h_size_k + space_size
            self.elements.append(move_left)

        self.cancel_btn = Button(uid=f'cancel_{slot}_btn', text='X',
                                    v_size_k=v_size,
                                    h_size_k=h_size_k, x_k=x_k,
                                    style=get_red_btn_style(),
                                    on_click_action=self.cancel_func,
                                    parent=self)
        self.elements.append(self.cancel_btn)
        x_k += h_size_k + space_size

        if right_active:
            move_right = Button(uid=f'move_right_{slot}_btn', text='->',
                                v_size_k=v_size,
                                h_size_k=h_size_k, x_k=x_k,
                                parent=self)
            self.elements.append(move_right)

        self.elements: Tuple[Button] = tuple(self.elements)

        # TODO cancel skip

        self.skip_btn: Button = Button(parent=self,
                                       uid=f'skip_{slot}', text='skip',
                                       on_click_action=self.skip_func)
        self.skip_btn_pos = (self.slot_rect.x, self.slot_rect.y + self.slot_rect.height // 2 - self.skip_btn.height // 2)
        self.skip_btn.move(self.skip_btn_pos)

    def skip_func(self, b: Button):
        Global.connection.send_json({GSC.SkillM.SkipCommand: self.slot})
    def cancel_func(self, b: Button):
        Global.connection.send_json({GSC.SkillM.CancelSkillUse: (self.slot, )})
    def render(self):
        self.surface.fill((0, 0, 0, 0))
        for el in self.elements:
            el.draw()

        return self
    def build(self):
        self.init_surface()
        self.render()

    def update(self):
        if self.rect.collidepoint(*Global.mouse.pos):
            for i, el in enumerate(self.elements):
                if el.collide_point(Global.mouse.pos):
                    self.draw_border_around_element(el)
                    if Global.mouse.l_up:
                        el.do_action()

    def init_surface(self):
        self.surface = get_surface(self.h_size, self.v_size, transparent=1)

    def draw(self):
        Global.display.blit(self.surface, self.real_position)

    def update_skip_btn(self):
        if self.skip_btn.collide_point(Global.mouse.pos):
            self.draw_border_around_element(self.skip_btn)
            if Global.mouse.l_up:
                self.skip_btn.do_action()

    def draw_skip_btn(self):
        Global.display.blit(self.skip_btn.surface, self.skip_btn_pos)

class UsedCardsC:
    player: PlayerObj
    cards_dy: int
    CARDS_MOVE_SPEED: int

    def __init__(self):
        self.used_cards_back_surface = None
        self.used_cards_positions_dict: Dict[int, Rect] = {}
        self.used_cards_dict: Dict[int, SkillCard] = {}
        self.used_cards_buttons: List[MoveCancelEl] = []
        self.__render()

    def __render(self):
        self.used_cards_back_surface = Surface(UsedCards.size)
        self.used_cards_back_surface.fill((100, 100, 100))

        self.__render_used_cards_rects()

        draw_rect(self.used_cards_back_surface, (255, 255, 255), (0, 0, UsedCards.h_size, UsedCards.v_size), 1)

    def __render_used_cards_rects(self) -> list:
        rects = []
        actions_num = self.processor.settings.actions_count
        free_size = UsedCards.h_size - actions_num * SkillCardSize.X_SIZE
        step = free_size / (actions_num + 1)
        x = 0 if free_size < 0 else step

        y = (UsedCards.v_size - SkillCardSize.Y_SIZE) // 2

        for i in range(actions_num):
            draw_rect(self.used_cards_back_surface,
                      (255, 255, 255),
                      (x, y, SkillCardSize.X_SIZE, SkillCardSize.Y_SIZE),
                      1,
                      SkillCard.default_style.border_radius)

            self.used_cards_positions_dict[i] = Rect(x + UsedCards.x, y + UsedCards.y,
                                                     SkillCardSize.X_SIZE, SkillCardSize.Y_SIZE)
            self.used_cards_dict[i] = None
            self.used_cards_buttons.append(MoveCancelEl(slot_rect=self.used_cards_positions_dict[i],
                                                        x=self.used_cards_positions_dict[i].x,
                                                        y=self.used_cards_positions_dict[i].y + SkillCardSize.Y_SIZE * 0.85,
                                                        h_size=SkillCardSize.X_SIZE,
                                                        v_size=SkillCardSize.Y_SIZE - SkillCardSize.Y_SIZE * 0.85,
                                                        slot=i,
                                                        left_active=i != 0,
                                                        right_active=i + 1 != actions_num).render())

            x += step
            x += SkillCardSize.X_SIZE

        return rects

    def draw_used_cards(self):
        # if self.used_cards_collide_point(Global.mouse.pos):
        Global.display.blit(self.used_cards_back_surface, (UsedCards.x, UsedCards.y))
        for i, action in self.player.scenario.actions.items():
            if action:
                if action.skip:
                    s = get_surface(SkillCardSize.X_SIZE, SkillCardSize.Y_SIZE, transparent=1, color=(50, 50, 170, 50))
                    Global.display.blit(s, self.used_cards_positions_dict[i].topleft)
                    Global.display.blit(self.used_cards_buttons[i].cancel_btn.surface, self.used_cards_buttons[i].cancel_btn.real_position )
                    if self.used_cards_buttons[i].cancel_btn.collide_point(Global.mouse.pos) and Global.mouse.l_up:
                        self.used_cards_buttons[i].cancel_btn.do_action()

                else:
                    card = self.skills_deck_dict[action.skill_uid]
                    Global.display.blit(card.surface, self.used_cards_positions_dict[i].topleft)
                    self.used_cards_buttons[i].draw()
                    self.used_cards_buttons[i].update()
                    if not action.valid:
                        Global.display.blit(card.invalid_surface, self.used_cards_positions_dict[i].topleft)

            else:
                self.used_cards_buttons[i].draw_skip_btn()
                self.used_cards_buttons[i].update_skip_btn()

    def used_cards_move_check(self):
        if HpBar.y + self.cards_dy < UsedCards.y + UsedCards.v_size:
            self.cards_dy += Global.clock.d_time * self.CARDS_MOVE_SPEED
            if HpBar.y + self.cards_dy > UsedCards.y + UsedCards.v_size:
                self.cards_dy = UsedCards.y + UsedCards.v_size - HpBar.y

    def used_cards_collide_point(self, pos: tuple) -> bool:
        return Rect(UsedCards.x, UsedCards.y, UsedCards.h_size, UsedCards.v_size).collidepoint(*pos)
