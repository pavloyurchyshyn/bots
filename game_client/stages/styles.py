from settings.screen.size import scaled_w
from visual.UI.constants.attrs import ButtonAttrs, TextAttrs


def update_btn_style(b):
    b['kwargs'].update({
        TextAttrs.RawText: False,
        ButtonAttrs.AutoDraw: False,
        ButtonAttrs.SurfaceColor: (10, 10, 25),
        ButtonAttrs.InacSurfaceColor: (5, 5, 10),
    })

    text_style = {
        TextAttrs.FontSize: scaled_w(0.01),
    }
    if b['kwargs'].get(TextAttrs.TextKwargs):
        b['kwargs'][TextAttrs.TextKwargs].update(text_style)
    else:
        b['kwargs'][TextAttrs.TextKwargs] = text_style

    inactext_style = {
        TextAttrs.FontSize: scaled_w(0.01),
    }
    if b['kwargs'].get(ButtonAttrs.InacTextKwargs):
        b['kwargs'][ButtonAttrs.InacTextKwargs].update(inactext_style)
    else:
        b['kwargs'][ButtonAttrs.InacTextKwargs] = inactext_style


def update_btn_size(b):
    b['kwargs'].update({
        ButtonAttrs.HSizeK: 0.1,
        ButtonAttrs.VSizeK: 0.05,
    })
