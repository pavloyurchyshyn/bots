from abc import abstractmethod
from visual.UI.base.menu import Menu


class Processor:
    UI: Menu

    @abstractmethod
    def connect(self, response: dict):
        raise NotImplementedError

    @abstractmethod
    def process_request(self, r: dict):
        raise NotImplementedError

    @abstractmethod
    def update(self):
        raise NotImplementedError
