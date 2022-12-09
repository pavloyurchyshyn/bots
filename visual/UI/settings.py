from pygame import SRCALPHA
from visual.UI.constants.colors import CommonColors
from settings.graphic import GraphicConfig


class UIDefault:
    Color = (255, 255, 255)

    class CollidedElBorder:
        r_0 = 0
        g_0 = 0
        b_0 = 200

        r_1 = 100
        g_1 = 100
        b_1 = 56

    TextColor = CommonColors.white
    TextBackColor = None
    InacTextColor = CommonColors.grey
    BorderColor = CommonColors.white
    InacBorderColor = CommonColors.grey
    BorderSize: int = 1
    BorderRadius: int = 3
    BorderTopLeftRadius: int = -1
    BorderTopRightRadius: int = -1
    BorderBottomLeftRadius: int = -1
    BorderBottomRightRadius: int = -1

    SurfaceTransparent = 1
    SurfaceFlags = SRCALPHA
    SurfaceColor = (0, 0, 0, 0)
    InacSurfaceColor = (0, 0, 0, 0)
    FromLeft: bool = False
    FromBot: bool = False
    FromTop: bool = False
    AA = GraphicConfig.Antialiasing
    AAText = GraphicConfig.AntialiasingText
