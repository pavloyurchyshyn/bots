from time import time as current_time
from settings.json_configs_manager import save_to_common_config, get_and_save_from_common_config

GLOBAL_SETTINGS = {
    'slow_motion': 0,
    'slow_motion_value': 0.05,
    'fps_config': get_and_save_from_common_config('fps_config', 60),
    'language': get_and_save_from_common_config('language', 'eng'),
    'scroll_speed': 5,
    'texture_pack': 'default',
}


def save_settings_attr(attr: str):
    save_to_common_config(attr, GLOBAL_SETTINGS[attr])


def save_all_config():
    for k in GLOBAL_SETTINGS.keys():
        save_settings_attr(k)


def set_texture_pack(texture_pack):
    GLOBAL_SETTINGS['texture_pack'] = texture_pack


def get_texture_pack_name() -> str:
    return GLOBAL_SETTINGS['texture_pack']


def get_scroll_speed():
    return GLOBAL_SETTINGS['scroll_speed']


def set_scroll_speed(speed):
    GLOBAL_SETTINGS['scroll_speed'] = speed


def get_language():
    return GLOBAL_SETTINGS['language']


def set_language(lang):
    GLOBAL_SETTINGS['language'] = lang
    save_to_common_config('language', lang)


def set_fps(fps):
    GLOBAL_SETTINGS['fps_config'] = fps
    save_to_common_config('fps_config', fps)


def get_fps() -> int:
    return GLOBAL_SETTINGS['fps_config']


DEFAULT_SLOW_TIME_DURATION = 10


def set_slow_motion(value=DEFAULT_SLOW_TIME_DURATION):
    GLOBAL_SETTINGS['slow_motion'] = value


def update_slow_motion(d_time):
    if GLOBAL_SETTINGS['slow_motion'] > 0:
        GLOBAL_SETTINGS['slow_motion'] -= d_time


def get_slow_motion_k():
    if GLOBAL_SETTINGS['slow_motion'] > 0:
        return GLOBAL_SETTINGS['slow_motion_value']
    else:
        return 1


def pause_step():
    GLOBAL_SETTINGS['next_pause'] = GLOBAL_SETTINGS['pause_delay'] + current_time()


def change_test_draw_status():
    GLOBAL_SETTINGS['test_draw'] = not GLOBAL_SETTINGS['test_draw']


set_fps(GLOBAL_SETTINGS['fps_config'])
