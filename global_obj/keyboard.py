import os

from pygame import key as PG_KEYS
from pygame import constants, locals
from pygame.key import name as pg_get_key_name
from pygame.constants import K_F4, K_LALT

from settings.json_configs_manager import load_json_config, save_json_config

from settings.default_keys import DEFAULT_COMMAND_KEY
from settings.base import KEYS_CONFIG_FILE


class KeyUsingError(Exception):
    def __init__(self, used_key):
        self.key = used_key

    def __str__(self):
        return f'Already using: {self.key}'


class Keyboard:
    def __init__(self, logger):
        self.logger = logger
        self.key_str_to_command = self.get_config()
        self.fulfill_config()
        self.save_config()
        self.commands = []
        self.text = []
        self._pressed = PG_KEYS.get_pressed()
        self._esc = False
        self._enter = False
        self._space = False

    def get_config(self) -> dict:
        if os.path.exists(KEYS_CONFIG_FILE):
            config = {key: command for command, key in load_json_config(KEYS_CONFIG_FILE).items() if key}
        else:
            config = {key: command for command, key in DEFAULT_COMMAND_KEY.items()}
        self.logger.info(f'Loaded keyboard config: {config}')
        return config

    def fulfill_config(self):
        config = self.key_str_to_command
        if len(config) < len(DEFAULT_COMMAND_KEY):
            commands = set(config.values())
            for command, default_key in DEFAULT_COMMAND_KEY.items():
                if command not in commands:
                    if default_key in config:
                        config[command] = None
                    else:
                        config[command] = default_key
                elif type(default_key) is not str and default_key not in config:
                    config[command] = default_key

    def save_config(self):
        self.logger.info(f'New keys {self.key_str_to_command} saved to {KEYS_CONFIG_FILE}')
        save_json_config({v: k for k, v in self.key_str_to_command.items()}, KEYS_CONFIG_FILE)

    def process_event(self, event):
        key_str = pg_get_key_name(event.key)
        if command := self.get_command(k_str=key_str):
            self.commands.append(command)
        self.check_for_special_keys(key_str)

    def update(self):
        self._pressed = PG_KEYS.get_pressed()
        self.commands.clear()
        self.text.clear()
        self._esc = False
        self._enter = False
        self._space = False

    def get_command(self, k_str: str) -> str or None:
        return self.key_str_to_command.get(k_str)

    def check_for_special_keys(self, k_str: str) -> None:
        match k_str:
            case 'return':
                self._enter = 1
            case 'escape':
                self._esc = 1
            case 'space':
                self._space = 1

    @property
    def pressed(self):
        return self._pressed

    @property
    def SPACE(self):
        return self._space

    @property
    def ESC(self):
        return self._esc

    @property
    def ENTER(self):
        return self._enter

    @property
    def BACKSPACE(self):
        return self._pressed[constants.K_BACKSPACE]

    @property
    def alt_and_f4(self):
        return self._pressed[K_F4] and self._pressed[K_LALT]

    def test(self):
        print(self.__dict__)

    def __getattr__(self, item: str):
        return item.replace('_', '', 1) in self.text