from typing import Type
from abc import abstractmethod


class BaseValidator:
    error: Type[Exception]

    @staticmethod
    @abstractmethod
    def validate(*args, **kwargs) -> bool:
        raise NotImplementedError

    @classmethod
    def validate_error(cls, *args, **kwargs):
        if not cls.validate(*args, **kwargs):
            raise cls.error
