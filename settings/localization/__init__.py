import yaml
from os import listdir, path
from settings.common import get_language, set_language
from settings.base import LOCALIZATIONS_FOLDER
from global_obj.logger import get_logger
from utils.singleton import Singleton

LOGGER = get_logger()

NO_TEXT_MSG = 'no text'

TEXT_PATH_DELIMITER = '/-/'
PATH_SYMBOL = '@//'
__all__ = ['LocalizationLoader', 'build_path', 'TEXT_PATH_DELIMITER']


def build_path(*args: str):
    return f'{PATH_SYMBOL if not args[0].startswith(PATH_SYMBOL) else ""}{TEXT_PATH_DELIMITER.join(args)}'


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
        self.localization = {}
        self.load()

    def load(self):
        LOGGER.debug(f'Importing localization {self.country.upper()}')
        country = path.join(LOCALIZATIONS_FOLDER, self.country)
        for file in listdir(country):
            with open(path.join(country, file), encoding='utf8') as f:
                self.localization[file.replace('.yaml', '')] = yaml.safe_load(f)


class LocalizationLoader(metaclass=Singleton):
    memory = {}

    def __init__(self):
        l_f = LOCALIZATIONS_FOLDER
        p_c = '__pycache__'
        self.available_langs = [l for l in listdir(l_f) if
                                path.isdir(path.join(l_f, l)) and p_c not
                                in path.join(l_f, l)]
        LOGGER.info(f'Available langs: {", ".join(self.available_langs)}')
        self.current_language: str = get_language()
        self.loaded_languages = {

        }
        self.load_lang('eng')
        self.load_current_lang()

    def change_language(self, lang):
        self.current_language = lang
        set_language(lang)

    @property
    def localization(self):
        return self.loaded_languages[self.current_language].localization

    def load_lang(self, lang):
        if lang in self.loaded_languages:
            return

        LOGGER.debug(f'Loading {lang} language')
        self.loaded_languages[lang] = LocalizationConfig(lang)
        LOGGER.info(f'Language {lang} successfully loaded.')

    def reload_lang(self, lang):
        LOGGER.debug(f'Reloading {lang} language')
        self.loaded_languages[lang] = LocalizationConfig(lang)
        LOGGER.info(f'Language {lang} successfully reloaded.')

    def load_current_lang(self):
        self.load_lang(self.current_language)

    def get_text(self, path: str):
        return self.get_text_from_lang(path.replace(PATH_SYMBOL, '', 1), self.current_language)

    def get_text_from_lang(self, path: str, lang: str, no_text: str = NO_TEXT_MSG):
        key = (path, lang)
        if key not in LocalizationLoader.memory:
            text = self.loaded_languages[lang].localization
            for attr in path.split(TEXT_PATH_DELIMITER):
                text = text.get(attr, no_text)
                if type(text) is str:
                    break

            LocalizationLoader.memory[key] = text
            LOGGER.debug(f'Path {path} localization result: {LocalizationLoader.memory[key]}')

        return LocalizationLoader.memory[key]

    def get_text_with_localization(self, text: str) -> str:
        return ' '.join((self.get_text(txt) if txt.startswith(PATH_SYMBOL) else txt for txt in text.split(' ')))


    def get_text_wloc(self, text: str) -> str:
        return self.get_text_with_localization(text)


if __name__ == '__main__':
    l = LocalizationLoader()
    print(l.__dict__)
