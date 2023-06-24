from global_obj.main import Global
from pygame.draw import rect as draw_rect
from game_client.game_match.stages.match_menu.settings.windows_sizes import MechWin
from visual.UI.base.text import Text


class MechC:
    def __init__(self):
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
