from visual.UI.constants.attrs import ButtonAttrs

from global_obj import Global

from settings.localization.menus.UI import UI as UILoc

from game_client.stages.new_game.settings.uids import UIDs
from game_client.stages.styles import update_btn_style, update_btn_size


def back_func(b: ButtonAttrs):
    Global.stages.main_menu()


BUTTONS_DATA = {
    'new_game': {
        'kwargs': {
            ButtonAttrs.XK: 0.9,
            ButtonAttrs.YK: 0.945,
            ButtonAttrs.UID: UIDs.Start,
            ButtonAttrs.Text: UILoc.NewGameMenu.start,
            ButtonAttrs.OnClickAction: lambda b: b,
        }
    },
    'back': {
        'kwargs': {
            ButtonAttrs.XK: 0.975,
            ButtonAttrs.YK: 0.01,
            ButtonAttrs.HSizeK: 0.02,
            ButtonAttrs.RectSize: True,
            ButtonAttrs.UID: UIDs.Back,
            ButtonAttrs.Text: UILoc.NewGameMenu.back,
            ButtonAttrs.OnClickAction: back_func,
        }
    },
}

# for b in BUTTONS_DATA.values():
update_btn_style(BUTTONS_DATA['back'])
update_btn_style(BUTTONS_DATA['new_game'])
update_btn_size(BUTTONS_DATA['new_game'])
