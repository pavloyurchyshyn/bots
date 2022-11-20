from settings.localization import build_path
from settings.localization.menus.common import CommonText

UI_path = build_path('menus', 'UI')


class UI:
    class MainMenu:
        menu = build_path(UI_path, 'main_menu')
        MenuStart = build_path(menu, 'menu_start')
        Multiplayer = build_path(menu, 'multiplayer')
        Settings = build_path(menu, 'settings')
        Exit = build_path(menu, 'exit')
        ExitYes = CommonText.Yes
        ExitNo = CommonText.No
        HostGame = build_path(menu, 'host_game')
        LangDisappMsg = build_path(menu, 'lang_disapp_msg')
        NewGame = build_path(menu, 'new_game')
