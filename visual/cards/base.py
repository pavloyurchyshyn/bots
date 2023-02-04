from pygame import Surface
from core.shape import Vector2DType
from core.shape.rectangle import Rectangle
from visual.UI.base.element import DrawBorderMixin
from visual.UI.base.style import Style
from settings.visual.cards import CardSize
from global_obj.main import Global
from visual.UI.constants.colors import CommonColors


class Card(Rectangle, DrawBorderMixin):
    Colors = CommonColors
    default_style = Style(border_size=1)

    surface: Surface

    # TODO think about small surface
    def __init__(self, uid: str,
                 x, y,
                 style: Style = None,
                 size_x=CardSize.X_SIZE, size_y=CardSize.Y_SIZE):
        self.uid: str = uid
        super().__init__(x, y, size_x, size_y)
        self.style: Style = self.default_style if style is None else style
        self.chosen: bool = False

    def render(self):
        raise NotImplementedError

    def choose(self):
        self.chosen = True

    def unchoose(self):
        self.chosen = False

    def move_to(self, xy: Vector2DType, *args, **kwargs) -> None:
        self.move(xy)

    def draw(self, dx=0, dy=0):
        Global.display.blit(self.surface, (self.x0 + dx, self.y0 + dy))
