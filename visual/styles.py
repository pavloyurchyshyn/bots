from visual.UI.base.style import ButtonStyle
from visual.UI.constants.attrs import ButtonStyleAttrs as BtnSA, StyleAttrs as SA, TextAttrs
from settings.visual.ui_default import UIDefault


def get_btn_style(**kwargs) -> ButtonStyle:
    kwargs[SA.SurfaceColor.value] = kwargs.get(SA.SurfaceColor.value, UIDefault.ButtonSurfaceColor)
    kwargs[BtnSA.InacSurfaceColor.value] = kwargs.get(BtnSA.InacSurfaceColor.value, UIDefault.ButtonInacSurfaceColor)
    kwargs[SA.BorderColor.value] = kwargs.get(SA.BorderColor.value, UIDefault.ButtonBorderColor)
    kwargs[SA.BackgroundRadius.value] = kwargs.get(SA.BackgroundRadius.value, UIDefault.BackgroundRadius)

    return ButtonStyle(**kwargs)


DEFAULT_H_SIZE, DEFAULT_V_SIZE = 0.1, 0.05


def get_green_btn_style(**kwargs) -> ButtonStyle:
    kwargs[SA.SurfaceColor.value] = kwargs.get(SA.SurfaceColor.value, UIDefault.GreenButtonBackColor)
    kwargs[SA.SurfaceTransparent.value] = kwargs.get(SA.SurfaceTransparent.value, UIDefault.ButtonSurfaceTransparent)
    kwargs[SA.BorderColor.value] = kwargs.get(SA.BorderColor.value, UIDefault.GreenButtonBorderColor)
    kwargs[SA.BorderRadius.value] = kwargs.get(SA.BorderRadius.value, UIDefault.ButtonBorderRadius)
    kwargs[SA.BorderSize.value] = kwargs.get(SA.BorderSize.value, UIDefault.ButtonBorderSize)

    return ButtonStyle(**kwargs)


def get_red_btn_style(**kwargs) -> ButtonStyle:
    kwargs[SA.SurfaceColor.value] = kwargs.get(SA.SurfaceColor.value, (155, 50, 50))
    kwargs[SA.SurfaceTransparent.value] = kwargs.get(SA.SurfaceTransparent.value, True)
    kwargs[SA.BorderColor.value] = kwargs.get(SA.BorderColor.value, (255, 50, 50))
    kwargs[SA.BorderRadius.value] = kwargs.get(SA.BorderRadius.value, 3)
    kwargs[SA.BorderSize.value] = kwargs.get(SA.BorderSize.value, 3)

    return ButtonStyle(**kwargs)
