import os
import logging
from pathlib import Path
LOG_LEVEL = logging.WARNING

ROOT_OF_GAME = Path(os.getcwd())
TEXTURES_FOLDER = ROOT_OF_GAME / 'textures'
DEFAULT_TEXTURES_FOLDER = TEXTURES_FOLDER / 'default'
MAPS_SAVES = ROOT_OF_GAME / 'maps'
LOGS_FOLDER = ROOT_OF_GAME / 'logs'
SETTINGS_PATH = ROOT_OF_GAME / 'settings'
LOCALIZATIONS_FOLDER = ROOT_OF_GAME / 'localization'

SOUNDS_FOLDER = ROOT_OF_GAME / 'sounds'
SERVER_FOLDER = ROOT_OF_GAME / 'client_server_parts'

COMMON_CONFIG_PATH = SETTINGS_PATH / 'common_config.json'
KEYS_CONFIG_FILE = SETTINGS_PATH / 'keyboard_config.json'

for f in (SETTINGS_PATH, MAPS_SAVES):
    f.mkdir(exist_ok=True)
# patterns
LOG_FILE_PATTERN = os.path.join(LOGS_FOLDER, '{}.txt')
