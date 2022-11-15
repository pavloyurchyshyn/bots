import os

VERSION = '0.0.01'

# ROOT_OF_GAME = os.path.abspath(os.getcwd())
ROOT_OF_GAME = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

LOGS_FOLDER = os.path.join(ROOT_OF_GAME, 'logs')
SETTINGS_PATH = os.path.join(ROOT_OF_GAME, 'settings')
LOCALIZATIONS_FOLDER = os.path.join(ROOT_OF_GAME, 'localization')

SOUNDS_FOLDER = os.path.join(ROOT_OF_GAME, 'sounds')
SERVER_FOLDER = os.path.join(ROOT_OF_GAME, 'client_server_parts')

COMMON_CONFIG_PATH = os.path.join(SETTINGS_PATH, 'common_config.json')
KEYS_CONFIG_FILE = os.path.join(SETTINGS_PATH, 'keyboard_config.json')

for f in (LOGS_FOLDER, SETTINGS_PATH, SOUNDS_FOLDER, LOCALIZATIONS_FOLDER):
    if not os.path.exists(f):
        os.mkdir(f)
# patterns
LOG_FILE_PATTERN = os.path.join(LOGS_FOLDER, '{}_.txt')
