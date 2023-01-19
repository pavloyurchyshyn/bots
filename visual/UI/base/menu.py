from abc import abstractmethod
from typing import List
from global_obj.main import Global
from visual.UI.manager import UIManager
from visual.UI.base.button import Button
from visual.UI.base.mixins import CreateButtonMixin


class Menu(CreateButtonMixin):
    def __init__(self, buttons_data, surface=None):
        self.x, self.y = 0, 0
        self.surface = surface if surface else Global.display
        self.UI_manager = UIManager()
        self.buttons: List[Button] = self.create_button_from_data(buttons_data)
        self.UI_manager.add_elements(self.buttons)

    def simple_buttons_update(self, draw_border_func: callable = None):
        for b in self.buttons:
            b.draw()
            if b.active and b.collide_point(Global.mouse.pos):
                if draw_border_func:
                    draw_border_func(b)
                if Global.mouse.l_up:
                    b.do_action()

    @property
    def real_position(self) -> (int, int):
        return self.x, self.y

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
