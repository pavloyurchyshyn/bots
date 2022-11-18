from pygame import SRCALPHA
from visual.UI.constants.colors import CommonColors


class UIDefault:
    BorderColor = CommonColors.white
    BorderSize: int = 1
    BorderRadius: int = 0
    BorderTopLeftRadius: int = -1
    BorderTopRightRadius: int = -1
    BorderBottomLeftRadius: int = -1
    BorderBottomRightRadius: int = -1

    SurfaceTransparent = 1
    SurfaceFlags = SRCALPHA
    SurfaceColor = (0, 0, 0, 0)
