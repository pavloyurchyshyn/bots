from settings.localization import build_path
from settings.localization.menus.common import CommonText

UI_path = build_path('menus', 'UI')


class UILocal:

    class MainMenu:
        menu = build_path(UI_path, 'main_menu')
        MenuStart = build_path(menu, 'menu_start')
        Multiplayer = build_path(menu, 'multiplayer')
        Settings = build_path(menu, 'settings')
        MapEditor = build_path(menu, 'map_editor')
        Exit = build_path(menu, 'exit')
        ExitYes = CommonText.Yes
        ExitNo = CommonText.No
        HostGame = build_path(menu, 'host_game')
        LangDisappMsg = build_path(menu, 'lang_disapp_msg')
        NewGame = build_path(menu, 'new_game')
        LoadGame = build_path(menu, 'load_game')

    class NewGameMenu:
        new_game_menu = build_path(UI_path, 'new_game_menu')
        start = build_path(new_game_menu, 'start')
        back = build_path(new_game_menu, 'back')

    class JoinMenu:
        join_menu = build_path(UI_path, 'join_menu')
        join = build_path(join_menu, 'join')

    class Errors:
        errors = build_path('menus', 'errors')
        ConnectionLost = build_path(errors, 'connection_lost')
        UnknownError = build_path(errors, 'unknown')
