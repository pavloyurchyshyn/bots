from global_obj.main import Global
from visual.cards.skill.card import SkillCard
from core.mech.skills.skill import BaseSkill
from core.world.base.visual.world import VisualWorld
from core.mech.skills.constants import Targets
from core.validators.skill import ValidationError
from core.validators.constants import ValidationKeys
from server_stuff.constants.requests import GameStgConst as GSC


class BadTarget(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class UnknownTarget(Exception):
    pass


class CardUseC:
    cards_dy: int
    w: VisualWorld

    def __init__(self):
        self.selected_card_to_use: SkillCard = None
        self.good_target = False
        self._targets_validators: dict = {
            Targets.AnyMech: self.__mech_target,
            Targets.Tile: self.__tile_target,
            Targets.NoTarget: self.__no_target,
        }

    def check_for_card_use(self):
        self.good_target = False
        if self.selected_card_to_use:
            for target in self.selected_card_to_use.skill.targets:
                try:
                    use_skill_d = {GSC.SkillM.SkillUID: self.selected_card_to_use.skill.unique_id,
                                   GSC.SkillM.UseAttrs: {}
                                   }
                    self._targets_validators.get(target, self.__unknown_target)(skill=self.selected_card_to_use.skill,
                                                                                d=use_skill_d)
                except BadTarget as e:
                    if Global.mouse.l_up:
                        Global.logger.info(e.msg)
                except UnknownTarget:
                    Global.logger.warning(f'Unknown skill target "{target}"')
                    break
                else:
                    self.good_target = True
                    if Global.mouse.l_up:
                        Global.connection.send_json({GSC.SkillM.UseSkill: use_skill_d})

    @staticmethod
    def __unknown_target(d: dict, skill: BaseSkill):
        raise UnknownTarget

    def __no_target(self, d: dict, skill: BaseSkill):
        pass

    def __tile_target(self, d: dict, skill: BaseSkill):
        if self.w.window_rect.collidepoint(*Global.mouse.pos):
            tile = self.w.get_mouse_to_xy()
            # if not tile:
            #     raise BadTarget(f'No tile under mouse.')
            # elif not tile.passable:
            #     raise BadTarget(f'Tile {tile.id_xy} not passable.')
            # else:
            try:
                self.validate(skill=skill, **{ValidationKeys.TargetXYCoordinate: tile})
            except ValidationError as e:
                if Global.mouse.l_up:
                    self.chat.add_msg(e, text_kwargs=dict(color=(200, 200, 200)), raw_text=False)
                    Global.logger.info(f'Bad target for skill "{skill.name}" - {tile}, reason: {e}')
                raise BadTarget(e.msg)

            else:
                d[GSC.SkillM.UseAttrs][Targets.Tile] = tile

        else:
            raise BadTarget('Mouse outside of world window.')

    def validate(self, skill: BaseSkill, **additional_kwargs):
        return skill.validate_use(player=self.player,
                                  **Global.get_dict_for_validations(),
                                  **additional_kwargs,
                                  )

    def __mech_target(self, d: dict, skill: BaseSkill):
        pass

    def draw_use_trace(self):
        if self.selected_card_to_use:
            target_hex = self.w.get_tile_by_xy(self.w.get_mouse_to_xy())
            if target_hex:
                self.w.draw_ray_from_a_to_b(target_hex, self.w.get_tile_by_xy(self.mech.position),
                                            color=(0, 155, 0) if self.good_target else (255, 100,100), width=2)
