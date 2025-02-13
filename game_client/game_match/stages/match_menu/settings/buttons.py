from global_obj.main import Global
from visual.UI.base.button import Button
from visual.UI.yes_no_popup import YesNoPopUp
from visual.UI.constants.attrs import ButtonAttrs
from settings.localization.menus.UI import UILocal
from game_client.game_match.stages.match_menu.settings.uids import UIDs


def add_exit_popup(b: Button):
    menu_ui = b.parent
    menu_ui.add_popup(YesNoPopUp('leave_game_popup',
                                 text=UILocal.Match.LeaveGame,
                                 no_on_click_action=lambda n_b: n_b.parent.close(n_b),
                                 yes_on_click_action=lambda y_b: (y_b.parent.close(y_b),
                                                                  Global.stages.close_game(),
                                                                  ),
                                 )
                      )


BUTTONS_DATA = {
    'exit': {
        'kwargs': {
            ButtonAttrs.UID: UIDs.ExitBtn,
            ButtonAttrs.Text: 'X',
            ButtonAttrs.XK: 0.969,
            ButtonAttrs.YK: 0.001,
            ButtonAttrs.HSizeK: 0.03,
            ButtonAttrs.VSizeK: 0.025,
            ButtonAttrs.OnClickAction: add_exit_popup,
        }
    },
}
