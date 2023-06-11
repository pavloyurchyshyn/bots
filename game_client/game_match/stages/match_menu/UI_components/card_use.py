from typing import Tuple, Dict
from global_obj.main import Global
from visual.cards.skill.card import SkillCard
from core.mech.skills.skill import BaseSkill
from core.world.base.visual.world import VisualWorld
from core.mech.skills.constants import Targets
from core.validators.skill import ValidationError, NoEmptyStepError
from core.validators.constants import ValidationKeys
from server_stuff.constants.requests import GameStgConst as GSC
from core.world.base.hex_utils import HexMath
from settings.localization.menus.UI import UILocal
from settings.localization.validation import ValidationMsg as ValidationLoc


from core.functions.scenario import get_free_slot_id


def get_send_function(data: dict) -> callable:
    def func(b, invalid_use:bool = True, *_, **__):
        data[GSC.SkillM.UseSkill][GSC.SkillM.InvalidUse] = invalid_use
        Global.connection.send_json(data)
        b.parent.close(b)
    return func


class CardUseC:
    cards_dy: int
    w: VisualWorld

    def __init__(self):
        self.selected_card_to_use: SkillCard = None
        self.good_target = False
        self.draw_good_square = True

    def check_for_card_use(self):
        self.good_target = False
        if self.w.window_rect.collidepoint(*Global.mouse.pos) and self.selected_card_to_use:
            tile_xy = self.w.get_mouse_to_xy()

            if self.player.scenario.is_full and Global.mouse.l_up:
                self.add_ok_popup(ValidationLoc.NoEmptyStepError)
                return

            action_id = get_free_slot_id(player=self.player)
            use_skill_d = {GSC.SkillM.SkillUID: self.selected_card_to_use.skill.unique_id,
                           GSC.SkillM.ActionID: action_id,
                           GSC.SkillM.UseAttrs: {
                               Targets.Tile: tile_xy,
                                                 }
                           }
            request = {GSC.SkillM.UseSkill: use_skill_d}
            skill = self.selected_card_to_use.skill
            try:
                self.validate(skill=skill, target_xy_coord=tile_xy)
            except NoEmptyStepError:
                if Global.mouse.l_up:
                    self.add_ok_popup(ValidationLoc.NoEmptyStepError)
            except ValidationError as e:
                if Global.mouse.l_up:
                    self.add_yes_no_popup(f'{e} \n {UILocal.Match.UseNotValidSkill}', raw_text=False,
                                          yes_action=get_send_function(request))

                    self.chat.add_msg(e, text_kwargs=dict(color=(255, 100, 100)), raw_text=False, capitalize=True)
                    Global.logger.info(f'Bad target for skill "{skill.name}" - {tile_xy}, reason: {e}')
            else:
                self.good_target = True
                if self.player.scenario.has_slots:
                    if Global.mouse.l_up:
                        Global.logger.info(f'Using skill: {request}')
                        Global.connection.send_json(request)
                elif Global.mouse.l_up:
                    self.add_ok_popup(f'No free slots') # TODO localization


    def validate(self, skill: BaseSkill, mech=None,**additional_kwargs):
        mech = mech if mech else self.player.latest_scenario_mech
        return skill.validate_use(player=self.player,
                                  mech=mech,
                                  **Global.get_dict_for_validations(),
                                  **additional_kwargs,
                                  )

    def draw_use_trace(self):
        if self.selected_card_to_use:
            target_hex = self.w.get_tile_by_xy(self.w.get_mouse_to_xy())
            if target_hex:
                # TODO fix it if first slots are empty
                self.w.draw_ray_from_a_to_b(a_qr=target_hex,
                                            b_qr=self.w.get_tile_by_xy(self.player.latest_scenario_mech.position),
                                            color=(0, 155, 0) if self.good_target else (255, 100,100), width=2)
            if self.draw_good_square:
                tiles = HexMath.get_neighbors_qr(*self.w.get_tile_by_xy(self.player.latest_scenario_mech.position).qr,
                                                 self.selected_card_to_use.skill.cast_range)


                for tile in tiles:
                    if target_hex and tile == target_hex.qr:
                        continue
                    try:
                        tile = self.w.get_tile_by_qr(tile)
                        if tile:
                            self.validate(self.selected_card_to_use.skill, **{ValidationKeys.TargetXYCoordinate: tile.xy_id})
                    except:
                        pass
                    else:
                        self.w.draw_border_for_xy(tile.xy_id, width=2, color=(100, 225, 100))
