from time import time as current_time
from settings.json_configs_manager import get_from_common_config, save_to_common_config


GLOBAL_SETTINGS = {
    'test_draw': 0,
    'slow_motion': 0,
    'slow_motion_value': 0.05,
    'fps': get_from_common_config('fps_config', 10),
    'language': get_from_common_config('language', 'eng'),
    'scroll_speed': 5,
}


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
    GLOBAL_SETTINGS['fps'] = fps
    save_to_common_config('fps_config', fps)


def get_fps():
    return GLOBAL_SETTINGS['fps']


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


def test_draw_status_is_on():
    return GLOBAL_SETTINGS['test_draw']