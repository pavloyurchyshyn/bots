from visual.UI.manager import UIManager
from visual.UI.base.button import Button
from visual.UI.constants.attrs import ButtonAttrs, TextAttrs

from settings.localization.menus.UI import UI

from game_client.stages.main_menu.settings.uids import UIDs
from global_obj import Global
from game_client.stages.styles import update_btn_style, update_btn_size

MENU_UIDS = (
    UIDs.NewGame,
    UIDs.LoadGame,
    UIDs.HostGame,
    UIDs.JoinGame,
    UIDs.Settings,
    UIDs.Exit,
)


def mock_func(b):
    print(f'TODO: Clicked {b.uid}')


def test_draw_btn(b: Button):
    Global.test_draw = not Global.test_draw
    if Global.test_draw:
        b.surface = b.active_surface
    else:
        b.surface = b.inactive_surface


def test_func(b):
    b.parent.UI_manager.get_by_uid('solo_game_btn').switch_active()


def exit_btn_func(b):
    ui_manager: UIManager = b.parent.UI_manager
    for uid in MENU_UIDS:
        ui_manager.get_by_uid(uid).deactivate()
    ui_manager.get_by_uid(UIDs.ExitYes).make_active_and_visible()
    ui_manager.get_by_uid(UIDs.ExitNo).make_active_and_visible()


def yes_btn_func(b):
    Global.logger.info(f'Clicked Yes to exit in main menu.')
    Global.stages.close_game()


def no_btn_func(b):
    ui_manager: UIManager = b.parent.UI_manager
    for uid in MENU_UIDS:
        ui_manager.get_by_uid(uid).activate()
    ui_manager.get_by_uid(UIDs.ExitYes).make_inactive_and_invisible()
    ui_manager.get_by_uid(UIDs.ExitNo).make_inactive_and_invisible()


BUTTONS_DATA = {
    'solo_game': {
        'kwargs': {
            ButtonAttrs.YK: 0.2,
            TextAttrs.Text: UI.MainMenu.NewGame,
            ButtonAttrs.UID: UIDs.NewGame,
            # ButtonAttrs.Active: False,
            # TextAttrs.RawText: False,
            ButtonAttrs.OnClickAction: lambda b: Global.stages.solo_game_menu(),
        }
    },

    'load_solo_game': {
        'kwargs': {
            ButtonAttrs.YK: 0.3,
            TextAttrs.Text: 'Load Game',
            ButtonAttrs.UID: UIDs.LoadGame,
            # ButtonAttrs.Active: False,
            ButtonAttrs.OnClickAction: lambda b: Global.stages.solo_game_menu(),
        }
    },

    'host_game': {
        'kwargs': {
            ButtonAttrs.YK: 0.4,
            TextAttrs.Text: UI.MainMenu.HostGame,
            ButtonAttrs.UID: UIDs.HostGame,
            ButtonAttrs.OnClickAction: mock_func,
        }
    },

    'join_game': {
        'kwargs': {
            ButtonAttrs.YK: 0.5,
            TextAttrs.Text: UI.MainMenu.Multiplayer,
            ButtonAttrs.UID: UIDs.JoinGame,
            ButtonAttrs.OnClickAction: mock_func,
        }
    },

    'settings': {
        'kwargs': {
            ButtonAttrs.YK: 0.6,
            TextAttrs.Text: UI.MainMenu.Settings,
            ButtonAttrs.UID: UIDs.Settings,
            ButtonAttrs.OnClickAction: test_func,
        }
    },

    # 'about': {
    #     'kwargs': {
    #         ButtonAttrs.YK: 0.6,
    #         ButtonAttrs.Text: 'About',
    #         ButtonAttrs.UID: 'about_btn',
    #         ButtonAttrs.OnClickAction: lambda b: 1,
    #     }
    # },

    'exit': {
        'kwargs': {
            ButtonAttrs.YK: 0.7,
            TextAttrs.Text: UI.MainMenu.Exit,
            ButtonAttrs.UID: UIDs.Exit,
            ButtonAttrs.OnClickAction: exit_btn_func,
        }
    },
}

start_pos = 0.5

for button in BUTTONS_DATA.values():
    update_btn_style(button)
    update_btn_size(button)
    button['kwargs'][ButtonAttrs.YK] = start_pos
    start_pos += button['kwargs'][ButtonAttrs.VSizeK] + button['kwargs'][ButtonAttrs.VSizeK] * 0.15

BUTTONS_DATA['exit_yes'] = {
    "kwargs": {
        TextAttrs.Text: UI.MainMenu.ExitYes,
        ButtonAttrs.Layer: 1,
        ButtonAttrs.UID: UIDs.ExitYes,
        ButtonAttrs.XK: 0.39,
        ButtonAttrs.YK: 0.5,
        ButtonAttrs.Active: False,
        ButtonAttrs.Visible: False,
        ButtonAttrs.OnClickAction: yes_btn_func,
        ButtonAttrs.InactiveAfterClick: 1,
        ButtonAttrs.InvisAfterClick: 1,
    }
}

BUTTONS_DATA['exit_no'] = {
    "kwargs": {
        TextAttrs.Text: UI.MainMenu.ExitNo,
        ButtonAttrs.Layer: 1,
        ButtonAttrs.UID: UIDs.ExitNo,
        ButtonAttrs.XK: 0.51,
        ButtonAttrs.YK: 0.5,
        ButtonAttrs.Active: False,
        ButtonAttrs.Visible: False,
        ButtonAttrs.OnClickAction: no_btn_func,
        ButtonAttrs.InactiveAfterClick: 1,
        ButtonAttrs.InvisAfterClick: 1,
    }
}

update_btn_style(BUTTONS_DATA['exit_yes'])
update_btn_size(BUTTONS_DATA['exit_yes'])
update_btn_style(BUTTONS_DATA['exit_no'])
update_btn_size(BUTTONS_DATA['exit_no'])

BUTTONS_DATA['test_draw'] = {
    "kwargs": {
        TextAttrs.Text: '+',
        ButtonAttrs.Layer: 2,
        ButtonAttrs.UID: 'test_draw',
        ButtonAttrs.XK: 0.975,
        ButtonAttrs.YK: 0.01,
        ButtonAttrs.HSizeK: 0.02,
        ButtonAttrs.RectSize: 1,
        # ButtonAttrs.VSizeK: 0.04,
        ButtonAttrs.Active: Global.test_draw,
        ButtonAttrs.Visible: Global.test_draw,
        ButtonAttrs.OnClickAction: test_draw_btn,
    }
}
