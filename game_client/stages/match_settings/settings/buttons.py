
from global_obj import Global

from visual.UI.constants.attrs import ButtonAttrs

from settings.localization.menus.UI import UILocal

from game_client.stages.match_settings.settings.uids import UIDs
from game_client.stages.styles import get_default_btn_style, DEFAULT_V_SIZE, DEFAULT_H_SIZE


def back_func(b: ButtonAttrs):
    Global.stages.main_menu()


BUTTONS_DATA = {
    'new_game': {
        'kwargs': {
            ButtonAttrs.XK: 0.9,
            ButtonAttrs.YK: 0.945,
            ButtonAttrs.HSizeK: DEFAULT_H_SIZE,
            ButtonAttrs.VSizeK: DEFAULT_V_SIZE,
            ButtonAttrs.UID: UIDs.Start,
            ButtonAttrs.Text: UILocal.NewGameMenu.start,
            ButtonAttrs.OnClickAction: lambda b: b,
            ButtonAttrs.Style: get_default_btn_style(),
        }
    },
    'back': {
        'kwargs': {
            ButtonAttrs.XK: 0.975,
            ButtonAttrs.YK: 0.01,
            ButtonAttrs.HSizeK: 0.02,
            ButtonAttrs.RectSize: True,
            ButtonAttrs.UID: UIDs.Back,
            ButtonAttrs.Text: UILocal.NewGameMenu.back,
            ButtonAttrs.OnClickAction: back_func,
            ButtonAttrs.Style: get_default_btn_style(),
        }
    },
}

