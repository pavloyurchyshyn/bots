from global_obj.main import Global
from visual.cards.skill.card import SkillCard
from pygame.draw import rect as draw_rect, line as draw_line, circle as draw_circle
from core.world.base.visual.world import VisualWorld
from core.mech.base.skills.constants import Targets
from server_stuff.constants.requests import GameStgConst as GSC
from core.world.base.logic.tile import LogicTile


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
                    self._targets_validators.get(target, self.__unknown_target)(use_skill_d)
                except BadTarget as e:
                    Global.logger.warning(e.msg)
                except UnknownTarget:
                    Global.logger.warning(f'Unknown skill target "{target}"')
                    break
                else:
                    self.good_target = True
                    if Global.mouse.l_up:
                        Global.connection.send_json(
                            {GSC.SkillM.UseSkill: use_skill_d}
                        )
                        # TODO send request
                        pass

    @staticmethod
    def __unknown_target(d: dict):
        raise UnknownTarget

    def __no_target(self, d: dict):
        pass

    def __tile_target(self, d: dict):
        if self.w.window_rect.collidepoint(*Global.mouse.pos):
            tile = self.w.get_tile_under_mouse()
            if not tile:
                raise BadTarget(f'No tile under mouse.')
            elif not tile.passable:
                raise BadTarget(f'Tile {tile.id_xy} not passable.')
            else:
                d[GSC.SkillM.UseAttrs][Targets.Tile] = tile.id_xy

        else:
            raise BadTarget('Mouse outside of world window.')

    def __mech_target(self, d: dict):
        pass

    def draw_use_trace(self):
        if self.selected_card_to_use:
            draw_line(Global.display, (100, 255, 255),
                      self.selected_card_to_use.get_center(dy=self.cards_dy),
                      Global.mouse.pos,
                      4
                      )
            draw_circle(Global.display, (50, 255, 50) if self.good_target else (255, 50, 50), Global.mouse.pos, 5)
