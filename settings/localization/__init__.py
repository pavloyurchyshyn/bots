import yaml
from os import listdir, path
from settings.common import get_language
from settings.base import LOCALIZATIONS_FOLDER
from global_obj import Global
from utils.singleton import Singleton

LOGGER = Global.logger

NO_TEXT_MSG = 'no text'

TEXT_PATH_DELIMITER = '/./'
__all__ = ['LocalizationLoader', 'LOCAL', 'TEXT_PATH_DELIMITER']


class TextValue:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"!!! {self.value}"

    def __getattr__(self, name):
        return NO_TEXT_MSG


class LocalizationConfig:
    pattern = '{}\\{}.yaml'

    def __init__(self, language: str):
        self.country = language
        self.load()

    def load(self):
        LOGGER.info(f'Importing localization {self.country.upper()}')
        country = path.join(LOCALIZATIONS_FOLDER, self.country)
        for file in listdir(country):
            with open(path.join(country, file), encoding='utf8') as f:
                local_ = yaml.safe_load(f)
            if local_:
                for k, val in local_.items():
                    if type(val) is not dict:
                        setattr(self, k, val)
                    else:
                        self.parse_dict(k, val, self)
            else:
                LOGGER.warn(f'Failed to load: {file} for {self.country}')

    @staticmethod
    def parse_dict(key, value: dict, prev_obj):
        obj = TextValue(key)
        setattr(prev_obj, key, obj)
        for k, v in value.items():
            if type(v) is not dict:
                setattr(obj, k, v)
            else:
                LocalizationConfig.parse_dict(k, v, obj)

    def __getattr__(self, name):
        return NO_TEXT_MSG


class LocalizationLoader(metaclass=Singleton):
    memory = {}

    def __init__(self):
        l_f = LOCALIZATIONS_FOLDER
        p_c = '__pycache__'
        self.available_langs = [l for l in listdir(l_f) if
                                path.isdir(path.join(l_f, l)) and p_c not in path.join(l_f, l)]
        LOGGER.info(f'Available langs: {", ".join(self.available_langs)}')
        self._current_language = get_language()
        self.load_lang('eng')
        self.load_current_lang()

    def change_language(self, lang):
        self._current_language = lang

    @property
    def text(self):
        return getattr(self, self._current_language)

    def load_lang(self, lang):
        LOGGER.info(f'Loading {lang} language')
        setattr(self, lang, LocalizationConfig(lang))
        LOGGER.info(f'Language {lang} successfully loaded.')

    def load_current_lang(self):
        self.load_lang(self._current_language)

    def get_text(self, path):
        # LOGGER.info(f'Searching localization for {path}')
        key = (path, self._current_language)
        if key not in LocalizationLoader.memory:
            text = self.text
            for attr in path.split(TEXT_PATH_DELIMITER):
                text = getattr(text, attr)
                if text == NO_TEXT_MSG:
                    return text

            LocalizationLoader.memory[key] = text

        return LocalizationLoader.memory[key]

    def __getattr__(self, name):
        return NO_TEXT_MSG


LOCAL = LocalizationLoader()

if __name__ == '__main__':
    l = LocalizationLoader()
    print(l.__dict__)
