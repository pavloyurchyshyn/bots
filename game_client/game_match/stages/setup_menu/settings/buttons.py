from visual.UI.base.button import Button
from visual.UI.constants.attrs import ButtonAttrs
from game_client.game_match.stages.setup_menu.settings.uids import UIDs
from global_obj.main import Global
from game_client.stages.styles import get_btn_style, DEFAULT_V_SIZE, DEFAULT_H_SIZE
from settings.localization.menus.UI import UILocal
from server_stuff.constants.setup_stage import SetupStgConst as SSC


# TODO
def exit_to_main_menu(b: Button):
    Global.stages.close_game()


def start_game(b: Button):
    b.parent.setup_stage.send_start_request()


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
    'start': {
        'kwargs': {
            ButtonAttrs.XK: 0.9,
            ButtonAttrs.YK: 0.945,
            ButtonAttrs.HSizeK: DEFAULT_H_SIZE,
            ButtonAttrs.VSizeK: DEFAULT_V_SIZE,
            ButtonAttrs.UID: UIDs.Start,
            ButtonAttrs.Text: UILocal.NewGameMenu.start,
            ButtonAttrs.OnClickAction: start_game,
            ButtonAttrs.Style: get_btn_style(),
        }
    },
}
