from visual.UI.base.button import Button
from visual.UI.constants.attrs import Attrs
from core.game_global import GameGlobal
from settings.screen.size import scaled_w


class MenuAbs:
    solo_game: Button
    load_solo_game: Button
    exit: Button


main_menu_button_style = {
    Attrs.HSizeK: 0.1,
    Attrs.VSizeK: 0.05,
    Attrs.AutoDraw: False,
    Attrs.TextKwargs: {
        Attrs.FontSize: scaled_w(0.01),
    }
}

BUTTONS_DATA = {

    'solo_game': {
        'kwargs': {
            Attrs.YK: 0.2,
            Attrs.Text: 'New Game',
            Attrs.UID: 'solo_game_btn',
            Attrs.OnClickAction: lambda b: GameGlobal.stages.solo_game_menu(),
        }
    },

    'load_solo_game': {
        'kwargs': {
            Attrs.YK: 0.3,
            Attrs.Text: 'Load Game',
            Attrs.UID: 'load_solo_game_btn',
            Attrs.OnClickAction: lambda b: GameGlobal.stages.solo_game_menu(),
        }
    },

    'host_game': {
        'kwargs': {
            Attrs.YK: 0.4,
            Attrs.Text: 'Host game',
            Attrs.UID: 'host_game_btn',
            Attrs.OnClickAction: lambda b: 1,
        }
    },

    'join_game': {
        'kwargs': {
            Attrs.YK: 0.5,
            Attrs.Text: 'Join game',
            Attrs.UID: 'join_game_btn',
            Attrs.OnClickAction: lambda b: 1,
        }
    },

    'settings': {
        'kwargs': {
            Attrs.YK: 0.6,
            Attrs.Text: 'Settings',
            Attrs.UID: 'settings_btn',
            Attrs.OnClickAction: lambda b: 1,
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
            Attrs.Text: 'Exit',
            Attrs.UID: 'exit_btn',
            Attrs.OnClickAction: lambda b: GameGlobal.stages.close_game(),
        }
    },
}

start_pos = 0.5
for button in BUTTONS_DATA.values():
    button['kwargs'].update(main_menu_button_style)
    button['kwargs'][Attrs.YK] = start_pos
    start_pos += button['kwargs'][Attrs.VSizeK] + button['kwargs'][Attrs.VSizeK] * 0.1
