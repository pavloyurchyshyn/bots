from settings.localization import build_path


class CommonText:
    common = build_path('menus', 'common')
    Yes = build_path(common, 'yes')
    No = build_path(common, 'no')
    Ready = build_path(common, 'ready')
    Cancel = build_path(common, 'cancel')
    Ok = build_path(common, 'ok')
    PressSpace = build_path(common, 'press_space')
