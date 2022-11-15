import os

from pygame import key as PG_KEYS
from pygame import constants, locals
from pygame.key import name as pg_get_key_name
from pygame import KEYDOWN, KEYUP, TEXTINPUT
from pygame.constants import K_F4, K_LALT

from settings.json_configs_manager import load_json_config, save_json_config

from settings.default_keys import DEFAULT_COMMAND_KEY
from settings.base import KEYS_CONFIG_FILE


#
# class Keyboard:
#     def __init__(self):
#         if os.path.exists(KEYS_CONFIG_FILE):
#             self._command_to_key: dict = load_json_config(KEYS_CONFIG_FILE)
#             self._command_to_key = {k: v for k, v in self._command_to_key.items() if v}
#             if len(self._command_to_key) < len(DEFAULT_COMMAND_KEY):
#                 keys = DEFAULT_COMMAND_KEY.copy()
#                 keys.update(self._command_to_key)
#                 self._command_to_key = keys
#         else:
#             self._command_to_key = DEFAULT_COMMAND_KEY
#         self.save()
#
#         self._keys_to_command = {}
#         self.make_key_to_command_dict()
#
#         self._esc = False
#         self._enter = False
#         self._space = False
#
#         self._pressed = ()
#         self._only_commands = set()
#         self._text = []
#
#         self._last_raw_inp = ''
#
#         self.update()
#         self._previous_settings = [self._keys_to_command.copy()]
#
#     def make_key_to_command_dict(self):
#         self._keys_to_command = {key: command for (command, key) in self._command_to_key.items()}
#         LOGGER.info(f'Keys to command created: {self._keys_to_command}')
#
#     def restore_default(self):
#         self._command_to_key = DEFAULT_COMMAND_KEY
#         LOGGER.info('Default keys restored.')
#         self.make_key_to_command_dict()
#         self.save()
#
#     def safety_change(self, command, new_key):
#         if new_key in self._command_to_key.values():
#             for comm, key in self._command_to_key.items():
#                 if key == new_key and comm != command:
#                     raise KeyUsingError(comm)
#         else:
#             self._command_to_key[command] = new_key
#             self._previous_settings.append(self._keys_to_command.copy())
#             self.make_key_to_command_dict()
#             self.save()
#
#     def back_step(self):
#         if self._previous_settings:
#             self._command_to_key = self._previous_settings.pop(-1)
#             self.make_key_to_command_dict()
#             self.save()
#
#     def change(self, command, new_key):
#         LOGGER.info(f'Changing command {command} to  {new_key}')
#         if new_key:
#             for command_, k in self._command_to_key.items():
#                 if k == new_key and command_ != command:
#                     LOGGER.info(f'Command {command_} deleted.')
#                     self._command_to_key[command_] = None
#                     break
#
#         self._previous_settings.append(self._command_to_key.copy())
#         self._command_to_key[command] = new_key
#         LOGGER.info(f'Command {command} changed to {self._command_to_key[command]}')
#
#         self.make_key_to_command_dict()
#         self.save()
#
#     def save(self):
#         LOGGER.info(f'New keys {self._command_to_key} saved to {KEYS_CONFIG_FILE}')
#         save_json_config(self._command_to_key, KEYS_CONFIG_FILE)
#
#     def update(self):
#         self._text.clear()
#         self._last_raw_inp = None
#         self._pressed = KEYS.get_pressed()
#         self._esc = False
#         self._enter = False
#         self._space = False
#
#     def check_for_special_keys(self, event):
#         key_name = get_key_name(event.key)
#         if key_name == 'return':
#             self._enter = True
#         elif key_name == 'escape':
#             self._esc = True
#         elif key_name == 'space':
#             self._space = True
#
#     def add_command(self, event):
#         command = self._keys_to_command.get(get_key_name(event.key))
#         if command:
#             self._only_commands.add(command)
#         self._last_raw_inp = get_key_name(event.key)
#
#     def delete_command(self, event):
#         command = self._keys_to_command.get(get_key_name(event.key))
#         if command in self._only_commands:
#             self._only_commands.remove(command)
#
#     def get_commands_by_key(self, key):
#         return (command for command, key_ in self._command_to_key.items() if key_ == key)
#
#     @property
#     def last_raw_text(self) -> str:
#         return self._last_raw_inp
#
#     @property
#     def text(self) -> str:
#         if self._text:
#             return ''.join(self._text)
#         else:
#             return ''
#
#     @property
#     def commands(self):
#         return self._only_commands
#
#     @property
#     def pressed(self):
#         return self._pressed
#
#     @property
#     def SPACE(self):
#         return self._space
#
#     @property
#     def ESC(self):
#         return self._esc
#
#     @property
#     def ENTER(self):
#         return self._enter
#
#     @property
#     def BACKSPACE(self):
#         return self._pressed[constants.K_BACKSPACE]
#
#     def get_key_command_values(self):
#         return self._keys_to_command.items()
#
#     @property
#     def alt_and_f4(self):
#         return self._pressed[K_F4] and self._pressed[K_LALT]


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
