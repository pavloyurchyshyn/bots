from visual.UI.base.button import Button
from visual.UI.constants.attrs import Attrs
from visual.UI.manager import UIManager

from core.game_global import GameGlobal

from settings.screen.size import scaled_w
from settings.localization.menus.UI import UI

from game.stages.main_menu.settings.uids import UIDs

mock_func = lambda b: print(f'TODO: Clicked {b.uid}')


def test_func(b):
    b.parent.UI_manager.get_by_uid('solo_game_btn').switch_active()


MENU_UIDS = (
    UIDs.NewGame,
    UIDs.LoadGame,
    UIDs.HostGame,
    UIDs.JoinGame,
    UIDs.Settings,
    UIDs.Exit,
)


def exit_btn_func(b):
    ui_manager: UIManager = b.parent.UI_manager
    for uid in MENU_UIDS:
        ui_manager.get_by_uid(uid).deactivate()


class MenuAbs:
    solo_game: Button
    load_solo_game: Button
    host_game: Button
    join_game: Button
    settings: Button
    exit: Button


main_menu_button_style = {
    Attrs.HSizeK: 0.1,
    Attrs.VSizeK: 0.05,
    Attrs.RawText: False,
    Attrs.AutoDraw: False,
    Attrs.TextKwargs: {
        Attrs.FontSize: scaled_w(0.01),
    },
    Attrs.InacTextKwargs: {
        Attrs.FontSize: scaled_w(0.01),
    }
}

BUTTONS_DATA = {

    'solo_game': {
        'kwargs': {
            Attrs.YK: 0.2,
            Attrs.Text: UI.MainMenu.NewGame,
            Attrs.UID: UIDs.NewGame,
            Attrs.Active: False,
            Attrs.RawText: False,
            Attrs.OnClickAction: lambda b: GameGlobal.stages.solo_game_menu(),
        }
    },

    'load_solo_game': {
        'kwargs': {
            Attrs.YK: 0.3,
            Attrs.Text: 'Load Game',
            Attrs.UID: UIDs.LoadGame,
            Attrs.Active: False,
            Attrs.OnClickAction: lambda b: GameGlobal.stages.solo_game_menu(),
        }
    },

    'host_game': {
        'kwargs': {
            Attrs.YK: 0.4,
            Attrs.Text: UI.MainMenu.HostGame,
            Attrs.UID: UIDs.HostGame,
            Attrs.OnClickAction: mock_func,
        }
    },

    'join_game': {
        'kwargs': {
            Attrs.YK: 0.5,
            Attrs.Text: UI.MainMenu.Multiplayer,
            Attrs.UID: UIDs.JoinGame,
            Attrs.OnClickAction: mock_func,
        }
    },

    'settings': {
        'kwargs': {
            Attrs.YK: 0.6,
            Attrs.Text: UI.MainMenu.Settings,
            Attrs.UID: UIDs.Settings,
            Attrs.OnClickAction: test_func,
        }
    },

    # 'about': {
    #     'kwargs': {
    #         Attrs.YK: 0.6,
    #         Attrs.Text: 'About',
    #         Attrs.UID: 'about_btn',
    #         Attrs.OnClickAction: lambda b: 1,
    #     }
    # },

    'exit': {
        'kwargs': {
            Attrs.YK: 0.7,
            Attrs.Text: UI.MainMenu.Exit,
            Attrs.UID: UIDs.Exit,
            Attrs.OnClickAction: exit_btn_func,
        }
    },
}

start_pos = 0.5
for button in BUTTONS_DATA.values():
    button['kwargs'].update(main_menu_button_style)
    button['kwargs'][Attrs.YK] = start_pos
    start_pos += button['kwargs'][Attrs.VSizeK] + button['kwargs'][Attrs.VSizeK] * 0.15
