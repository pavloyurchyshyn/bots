from pygame import SRCALPHA
from visual.UI.constants.colors import CommonColors


class UIDefault:
    TextColor = CommonColors.white
    InacTextColor = CommonColors.grey
    BorderColor = CommonColors.white
    InacBorderColor = CommonColors.grey
    BorderSize: int = 1
    BorderRadius: int = 0
    BorderTopLeftRadius: int = -1
    BorderTopRightRadius: int = -1
    BorderBottomLeftRadius: int = -1
    BorderBottomRightRadius: int = -1

    SurfaceTransparent = 1
    SurfaceFlags = SRCALPHA
    SurfaceColor = (0, 0, 0, 0)
    InacSurfaceColor = (0, 0, 0, 0)
