from typing import List
import pygame
from pygame import Surface
from global_obj.main import Global
from pygame.draw import rect as draw_rect
from game_client.game_match.stages.match_menu.settings.windows_sizes import MechWin, EffectsRect
from visual.UI.base.text import Text
from core.entities.effects.base import BaseEffect

from core.mech.mech import BaseMech

class EffectHint:
    def __init__(self, x: int, y:int, text: str):
        self.x = x
        self.y = y
        self.text_obj: Text = Text(uid='', text=text)
        self.surface: Surface = Surface
class EffectsVisualStatus:
    def __init__(self, x: int, y: int, effect: BaseEffect, parent_surface: Surface = Global.display):
        self.x = x
        self.y = y
        self.effect: BaseEffect = effect
        self.rect: pygame.Rect = pygame.Rect(self.x, self.y, *EffectsRect.EffectIconRect.size)

        self.surface: Surface = Surface(EffectsRect.EffectIconRect.size)
        self.parent_surface: Surface = parent_surface

    def change_position(self, x, y):
        self.x, self.y = x, y
        self.rect: pygame.Rect = pygame.Rect(self.x, self.y, *EffectsRect.EffectIconRect.size)

    def draw(self):
        self.parent_surface.blit(self.surface, (self.x, self.y))

class MechC:
    def __init__(self):
        self.effects: List[EffectsVisualStatus] = []
        self.damage_image = None # TODO
        self.armor_image = None # TODO

        if self.processor:
            dmg_text = 'Damage: 0'
            armor_text = 'Armor: 0'
        else:
            dmg_text = str(self.player.latest_scenario_mech.damage)
            armor_text = str(self.player.latest_scenario_mech.damage)

        self.damage_stat_value: Text = Text(uid='damage_stat_text', text=dmg_text,
                                            x_k=MechWin.X_K + 0.001, y_k=MechWin.Y_K + MechWin.V_SIZE_K *0.9,
                                            h_size_k=MechWin.H_SIZE_K/2 -  0.002, v_size_k=MechWin.V_SIZE_K * 0.1)
        self.armor_stat_value: Text = Text(uid='armor_stat_text', text=armor_text,
                                            x_k=MechWin.X_K + 0.001 + MechWin.H_SIZE_K/2, y_k=MechWin.Y_K + MechWin.V_SIZE_K *0.9,
                                            h_size_k=MechWin.H_SIZE_K/2 -  0.002, v_size_k=MechWin.V_SIZE_K * 0.1)

    def draw_mech_win(self):
        draw_rect(Global.display, (255, 255, 255), MechWin.rect, 1)
        # TODO do it only at events
        if self.processor:
            self.damage_stat_value.change_text(f'Damage: {self.player.latest_scenario_mech.damage}')
            self.armor_stat_value.change_text(f'Armor: {self.player.latest_scenario_mech.armor}')
        self.damage_stat_value.draw()
        self.armor_stat_value.draw()

        draw_rect(Global.display, (255, 255, 255), EffectsRect.rect, 1, 0, 3, 3)


    def collect_effects(self):
        mech: BaseMech = self.player.latest_scenario_mech
