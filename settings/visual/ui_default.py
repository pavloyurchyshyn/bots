from pygame import SRCALPHA
from visual.UI.constants.colors import CommonColors
from settings.visual.graphic import GraphicConfig


class UIDefault:
    Color = (255, 255, 255)

    class CollidedElBorder:
        r_0 = 90
        g_0 = 90
        b_0 = 90

        r_1 = 120
        g_1 = 120
        b_1 = 255

    TextColor = CommonColors.white
    TextBackColor = None
    InacTextColor = CommonColors.grey
    BorderColor = CommonColors.white
    InacBorderColor = CommonColors.grey
    BorderSize: int = 2
    BackgroundRadius: int = 5
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

    # ------- Buttons ---------------
    ButtonSurfaceColor = (35, 95, 120)
    ButtonBorderColor = (0, 145, 170)

    ButtonInacSurfaceColor = (55, 55, 55)

    GreenButtonBackColor = (50, 155, 90)
    GreenButtonBorderColor = (0, 105, 0)
    ButtonBorderSize = 3
    ButtonBorderRadius = 3
    ButtonSurfaceTransparent = True

