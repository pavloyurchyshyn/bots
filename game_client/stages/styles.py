from visual.UI.base.style import ButtonStyle
from visual.UI.constants.attrs import ButtonStyleAttrs, StyleAttrs


def get_default_btn_style():
    return ButtonStyle(**{
        StyleAttrs.SurfaceColor.value: (10, 10, 25),
        ButtonStyleAttrs.InacSurfaceColor.value: (5, 5, 10),
    })


DEFAULT_H_SIZE, DEFAULT_V_SIZE = 0.1, 0.05
