from pygame.draw import rect as draw_rect

from global_obj.main import Global
from core.world.base.map_save import MapSave
from core.world.base.visual.world import VisualWorld

from visual.UI.base.menu import Menu
from visual.UI.base.container import Container
from visual.UI.base.pop_up import PopUpsController
from visual.UI.base.mixins import DrawElementBorderMixin


class GameMatch(Menu, PopUpsController, DrawElementBorderMixin):

    def __init__(self, match_stage):
        super(GameMatch, self).__init__({})
        PopUpsController.__init__(self)
        self.match_stage = match_stage

    def update(self):
        Global.display.fill((0, 0, 0))
