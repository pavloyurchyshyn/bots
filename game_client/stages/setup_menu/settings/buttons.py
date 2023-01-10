from visual.UI.base.button import Button
from game_client.stages.styles import get_green_btn_style
from visual.UI.constants.attrs import ButtonAttrs, TextAttrs
from game_client.stages.setup_menu.settings.uids import UIDs
from visual.UI.yes_no_popup import YesNoPopUp
from global_obj import Global
from game_client.stages.styles import get_btn_style, DEFAULT_V_SIZE, DEFAULT_H_SIZE
from settings.localization.menus.UI import UILocal

# TODO
def exit_to_main_menu(b: Button):
    Global.stages.close_game()


BUTTONS_DATA = {
    'exit': {
        'kwargs': {
            ButtonAttrs.UID: UIDs.Exit,
            ButtonAttrs.Text: 'X',
            ButtonAttrs.XK: 0.965,
            ButtonAttrs.YK: 0.005,
            ButtonAttrs.HSizeK: 0.03,
            ButtonAttrs.VSizeK: 0.04,
            ButtonAttrs.OnClickAction: exit_to_main_menu,
        }
    },
    'new_game': {
        'kwargs': {
            ButtonAttrs.XK: 0.9,
            ButtonAttrs.YK: 0.945,
            ButtonAttrs.HSizeK: DEFAULT_H_SIZE,
            ButtonAttrs.VSizeK: DEFAULT_V_SIZE,
            ButtonAttrs.UID: UIDs.Start,
            ButtonAttrs.Text: UILocal.NewGameMenu.start,
            ButtonAttrs.OnClickAction: lambda b: b,
            ButtonAttrs.Style: get_btn_style(),
        }
    },
}
