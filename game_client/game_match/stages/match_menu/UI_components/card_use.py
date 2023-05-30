from global_obj.main import Global
from visual.cards.skill.card import SkillCard
from core.mech.skills.skill import BaseSkill
from core.world.base.visual.world import VisualWorld
from core.mech.skills.constants import Targets
from core.validators.skill import ValidationError
from core.validators.constants import ValidationKeys
from server_stuff.constants.requests import GameStgConst as GSC


class CardUseC:
    cards_dy: int
    w: VisualWorld

    def __init__(self):
        self.selected_card_to_use: SkillCard = None
        self.good_target = False

    def check_for_card_use(self):
        self.good_target = False
        if self.w.window_rect.collidepoint(*Global.mouse.pos) and self.selected_card_to_use:
            use_skill_d = {GSC.SkillM.SkillUID: self.selected_card_to_use.skill.unique_id,
                           GSC.SkillM.UseAttrs: {}
                           }
            tile_xy = self.w.get_mouse_to_xy()
            skill = self.selected_card_to_use.skill
            try:
                self.validate(skill=skill, **{ValidationKeys.TargetXYCoordinate: tile_xy} )
            except ValidationError as e:
                if Global.mouse.l_up:
                    self.chat.add_msg(e, text_kwargs=dict(color=(255, 100, 100)), raw_text=False, capitalize=True)
                    Global.logger.info(f'Bad target for skill "{skill.name}" - {tile_xy}, reason: {e}')
            else:
                self.good_target = True
                use_skill_d[GSC.SkillM.UseAttrs][Targets.Tile] = tile_xy
                if Global.mouse.l_up:
                    Global.connection.send_json({GSC.SkillM.UseSkill: use_skill_d})

    def validate(self, skill: BaseSkill, **additional_kwargs):
        return skill.validate_use(player=self.player,
                                  **Global.get_dict_for_validations(),
                                  **additional_kwargs,
                                  )

    def draw_use_trace(self):
        if self.selected_card_to_use:
            target_hex = self.w.get_tile_by_xy(self.w.get_mouse_to_xy())
            if target_hex:
                self.w.draw_ray_from_a_to_b(a_qr=target_hex, b_qr=self.w.get_tile_by_xy(self.mech.position),
                                            color=(0, 155, 0) if self.good_target else (255, 100,100), width=2)
