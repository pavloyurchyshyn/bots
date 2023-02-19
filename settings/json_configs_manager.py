import json
from os.path import exists
from settings.base import COMMON_CONFIG_PATH
from global_obj.logger import get_logger

LOGGER = get_logger()


def load_json_config(path: str) -> dict:
    if not exists(path):
        return {}

    with open(path, 'r') as k_conf:
        return json.load(k_conf)


def change_parameter_in_json_config(key, value, path):
    j = load_json_config(path)
    j[key] = value
    save_json_config(j, path)
    LOGGER.debug(f'Parameter {key} changed to {value} in {path}')


def get_parameter_from_json_config(key, path, def_value=None):
    return load_json_config(path).get(key, def_value)


def save_json_config(data: dict, path: str) -> None:
    with open(path, 'w') as k_conf:
        json.dump(data, k_conf)
    LOGGER.debug(f'Saved {data} to {path}')


def save_to_common_config(key, value):
    change_parameter_in_json_config(key, value, COMMON_CONFIG_PATH)


def get_from_common_config(key, def_value=None):
    return get_parameter_from_json_config(key=key, def_value=def_value, path=COMMON_CONFIG_PATH)


def get_common_config():
    return load_json_config(COMMON_CONFIG_PATH)


def save_common_config(data):
    save_json_config(data=data, path=COMMON_CONFIG_PATH)
