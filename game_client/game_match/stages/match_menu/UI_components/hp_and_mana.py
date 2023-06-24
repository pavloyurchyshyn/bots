from pygame import Surface
from typing import Tuple
from pygame.rect import Rect
from global_obj.main import Global
from pygame.draw import rect as draw_rect
from game_client.game_match.stages.match_menu.settings.windows_sizes import HpBar, ManaBar
# from visual.UI.base.element import BaseUI, GetSurfaceMixin, DrawBorderMixin
from visual.UI.utils import get_surface
from visual.UI.base.text import Text

class BaseUIBar:# (BaseUI, DrawBorderMixin):
    def __init__(self, uid: str, rect: Rect,
                 value: int, max_value: int,
                 rect_round: int = 3,
                 background_color=(50, 50, 50),
                 bar_color=(150, 150, 150),
                 border_color=(250, 250, 250),
                 **kwargs):
        # super().__init__(uid=uid, **kwargs)
        self.uid: str = uid
        self.value: int = value
        self.max_value: int = max_value

        self.rect: Rect = rect
        self.x: int = rect.x
        self.y: int = rect.y
        self.h_size, self.v_size = rect.size

        self.rect_round: int = rect_round

        self.background_color: Tuple[int, int, int] = background_color
        self.bar_color: Tuple[int, int, int] = bar_color
        self.border_color: Tuple[int, int, int] = border_color
        self.surface: Surface = get_surface(h_size=self.h_size, v_size=self.v_size, transparent=1)

    def change_value(self, value: int):
        if value != self.value:
            self.value = value
            self.render()

    def change_max_value(self, max_value: int):
        if max_value != self.max_value:
            self.max_value = max_value
            self.render()

    def render(self):
        self.surface.fill((0, 0, 0, 0))
        draw_rect(self.surface, self.background_color, (0, 0, self.h_size, self.v_size),
                  width=0, border_radius=self.rect_round)
        draw_rect(self.surface, self.bar_color, (0, 0, self.h_size * (self.value / self.max_value), self.v_size), 0, self.rect_round)
        draw_rect(self.surface, self.border_color, (0, 0, self.h_size, self.v_size), 1, self.rect_round)

    def draw(self, dx: int = 0, dy: int = 0):
        Global.display.blit(self.surface, (self.x + dx, self.y + dy))

class HpAndManaC:
    def __init__(self):
        self.hp_bar: BaseUIBar = BaseUIBar('hp_bar',
                                           bar_color=(0, 155, 0),
                                           background_color=(50, 100, 50),
                                           rect=Rect(HpBar.x, HpBar.y, HpBar.h_size, HpBar.v_size),
                                           value=1, max_value=2)
        self.hp_bar.render()

        self.hp_text: Text = Text(uid='hp_bar_text', text='2', raw_text=1,
                                  x_k=HpBar.X_K, y_k=HpBar.Y_K,
                                  h_size_k=HpBar.H_SIZE_K/5, v_size_k=HpBar.V_SIZE_K)

        self.energy_bar: BaseUIBar = BaseUIBar('energy_bar',
                                           bar_color=(0, 0, 155),
                                           background_color=(50, 50, 100),
                                           rect=Rect(ManaBar.x, ManaBar.y, ManaBar.h_size, ManaBar.v_size),
                                           value=1, max_value=2)
        self.energy_bar.render()

        self.energy_text: Text = Text(uid='energy_bar_text', text='2', raw_text=1,
                                  x_k=ManaBar.X_K, y_k=ManaBar.Y_K,
                                  h_size_k=ManaBar.H_SIZE_K/5, v_size_k=ManaBar.V_SIZE_K)

    def draw_hp_and_mana_win(self):
        if self.mech:
            # TODO do it only at events
            self.hp_bar.change_value(self.player.latest_scenario_mech.health_points)
            self.hp_bar.change_max_value(self.player.latest_scenario_mech.max_health_point)
            text = f'{self.player.latest_scenario_mech.health_points}/{self.player.latest_scenario_mech.max_health_point}'
            self.hp_text.change_text(text)

            self.energy_bar.change_value(self.player.latest_scenario_mech.energy)
            self.energy_bar.change_max_value(self.player.latest_scenario_mech.max_energy)
            text = f'{self.player.latest_scenario_mech.energy}/{self.player.latest_scenario_mech.max_energy}'
            self.energy_text.change_text(text)

        self.hp_bar.draw(dy=self.cards_dy)
        self.energy_bar.draw(dy=self.cards_dy)
        self.hp_text.draw(dy=self.cards_dy)
        self.energy_text.draw(dy=self.cards_dy)
