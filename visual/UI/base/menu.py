from abc import abstractmethod
from visual.UI.manager import UIManager
from visual.UI.base.button import Button
from global_obj import Global


class Menu:
    def __init__(self, buttons_data, surface=None):
        self.x, self.y = 0, 0
        self.surface = surface if surface else Global.display
        self.UI_manager = UIManager()
        self.buttons = self.create_button_from_data(buttons_data)

    def create_button_from_data(self, buttons_data: dict):
        buttons = []
        for button_name, button_data in buttons_data.items():
            b = Button(*button_data.get('args', ()),
                       **button_data.get('kwargs', {}),
                       parent=self)
            buttons.append(b)
            setattr(self, button_name, b)

        buttons.sort(key=lambda e: e.y, reverse=True)
        buttons.sort(key=lambda e: e.layer, reverse=True)

        return buttons

    @abstractmethod
    def update(self):
        raise NotImplementedError

    @staticmethod
    def __sort_value(element):
        """
        For sort.

        :param element: Rectangle or Circle object
        :return:
        """
        return element.y
